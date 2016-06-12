from pymongo import MongoClient
import argparse
from tweet_cleaner import TweetCleaner

def main(args):
    host = args.host
    port = args.port
    database = args.database
    collection = args.collection

    client = MongoClient(host=host, port=port)
    db = client[database]
    coll = db[collection]

    cursor = coll.find()

    tc = TweetCleaner()
    counter = 0
    for doc in cursor:
        if 'http' in doc['text']:
            cleaned = tc.clean(doc['text'])
            print doc['text']
            print cleaned
            print '\n'
            counter += 1
        if counter > 1000:
            break


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Import data into a MongoDB collection')
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=27017)
    parser.add_argument('--database', type=str)
    parser.add_argument('--collection', type=str)
    args = parser.parse_args()
    main(args)