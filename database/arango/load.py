import json

from arango import ArangoClient

if __name__ == '__main__':

    client = ArangoClient(hosts='http://localhost:8529')

    sys_db = client.db('_system', username='root', password='no-password')

    wiktionary_database = "wiktionary"
    if not sys_db.has_database(wiktionary_database):
        sys_db.create_database(wiktionary_database)
    db = client.db(wiktionary_database, username='root', password='no-password')

    german_collection = "German"
    if db.has_collection(german_collection):
        collection = db.collection(german_collection)
    else:
        collection = db.create_collection(german_collection)

    collection.add_index({'type': 'persistent', 'fields': ['term'], 'unique': False})
    collection.truncate()

    with open("../../german-wiktextract-data.jsonl", 'r', encoding='utf-8') as f:
        for line in f:
            try:
                json_object = json.loads(line.strip())
                collection.insert({
                    'term': json_object["term"],
                    'definitions': json_object["definitions"]
                })
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON on line: {line.strip()} - {e}")
