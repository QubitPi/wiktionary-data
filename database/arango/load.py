import json

from arango import ArangoClient


def load_by_language(language: str, jsonl_path: str):
    german_collection = language
    if db.has_collection(german_collection):
        collection = db.collection(german_collection)
    else:
        collection = db.create_collection(german_collection)

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
        load_by_language(language, jsonl_path)
