import argparse
from pymongo import MongoClient


def main(args):
    host = args.host
    port = args.port
    database = args.database
    collection = args.collection

    client = MongoClient(host=host, port=port)
    db = client[database]
    coll = db[collection]

    coll.create_index([('text', 'text')], name='tweet_text_index')

    print 'Index created'

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Create indices on MongoDB collection')
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=27017)
    parser.add_argument('--database', type=str)
    parser.add_argument('--collection', type=str)
    args = parser.parse_args()
    main(args)
