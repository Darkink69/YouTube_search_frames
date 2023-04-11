from pymongo import MongoClient


def load_mongo_data_url(field):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['urldb']
    collection = db['mongourls']
    items = collection.find()
    ids = []
    for item in items:
        if not item[field]:
            ids.append(item['id'])
    return ids


