import argparse
from pymongo import MongoClient
import pymongo
import random


def main(args):
    host = args.host
    port = args.port
    database = args.database
    collection = args.collection
    test_collection = args.test_collection
    test_proportion = args.test_proportion

    client = MongoClient(host=host, port=port)
    db = client[database]
    coll = db[collection]
    test_coll = db[test_collection]

    print "Creating index on test collection"

    test_coll.create_index([('id', pymongo.ASCENDING)], unique=True, name='id_unique_index')

    print "Created index on test collection"

    print "Dumping random docs into test collection"

    cursor = coll.find()

    for doc in cursor:
        if random.random() < test_proportion:
            test_coll.insert_one(doc)

    print "Test collection ready"

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Import data into a MongoDB collection')
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=27017)
    parser.add_argument('--database', type=str)
    parser.add_argument('--collection', type=str)
    parser.add_argument('--test_collection', type=str)
    parser.add_argument('--test_proportion', type=float)
    args = parser.parse_args()
    main(args)
