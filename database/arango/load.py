# Copyright 2025 Jiaqi Liu. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from multiprocessing import Process

from arango import ArangoClient


def load_by_language(language: str, jsonl_path: str):
    if db.has_collection(language):
        collection = db.collection(language)
    else:
        collection = db.create_collection(language)

    collection.add_index({'type': 'persistent', 'fields': ['term'], 'unique': False})
    collection.truncate()

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                json_object = json.loads(line.strip())
                collection.insert({
                    'term': json_object["term"],
                    'definitions': json_object["definitions"]
                })
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line.strip()} - {e}")


if __name__ == '__main__':
    client = ArangoClient(hosts='http://localhost:8529')

    sys_db = client.db('_system', username='root', password='no-password')

    wiktionary_database = "wiktionary"
    if not sys_db.has_database(wiktionary_database):
        sys_db.create_database(wiktionary_database)
    db = client.db(wiktionary_database, username='root', password='no-password')

    processes = []

    for language, jsonl_path in [
        ("German", "../../german-wiktextract-data.jsonl"),
        ("Latin", "../../latin-wiktextract-data.jsonl"),
        ("AncientGreek", "../../ancient-greek-wiktextract-data.jsonl"),
        ("Korean", "../../korean-wiktextract-data.jsonl"),
        ("OldPersian", "../../old-persian-wiktextract-data.jsonl"),
        ("Akkadian", "../../akkadian-wiktextract-data.jsonl"),
        ("Elamite", "../../elamite-wiktextract-data.jsonl"),
        ("Sanskrit", "../../sanskrit-wiktextract-data.jsonl"),
    ]:
        process = Process(target=load_by_language, args=(language, jsonl_path))
        process.start()
        processes.append(process)

    for process in processes:
        process.join()
