from pymongo import MongoClient


def load_mongo_data(id, field):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['urldb']
    collection = db['mongourls']
    items = collection.find()
    data = []
    for item in items:
        if id in item['id']:
            data.append(item[field])

    return data
