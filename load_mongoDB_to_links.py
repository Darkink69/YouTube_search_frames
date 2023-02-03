from pymongo import MongoClient


def load_mongo_data_url(field):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['urldb']
    collection = db['mongourls']
    items = collection.find()
    links = []
    for item in items:
        if not item[field]:
            links.append(item['url'])
    # print(links)
    return links


