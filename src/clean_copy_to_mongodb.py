from pymongo import MongoClient
import pymongo
import argparse
from tweet_cleaner import TweetCleaner


DATA_DIRECTORY = '../data'
ARCHIVE_DIRECTORY = '../data-archive'


def main(args):
    host = args.host
    port = args.port
    database = args.database
    source_collection = args.src_collection
    dest_collection = args.dest_collection

    client = MongoClient(host=host, port=port)
    db = client[database]
    src_coll = db[source_collection]
    dest_coll = db[dest_collection]

    src_cursor = src_coll.find()

    tc = TweetCleaner()

    print "Copy started"
    counter = 0
    for doc in src_cursor:
        cleaned_tweet = tc.clean(doc['text'])
        dest_coll.insert_one({'text': cleaned_tweet})
        counter += 1
        if counter % 1000 == 0:
            print "{0} tweets copied".format(counter)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Clean and copy data into a MongoDB collection')
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=27017)
    parser.add_argument('--database', type=str)
    parser.add_argument('--src_collection', type=str)
    parser.add_argument('--dest_collection', type=str)
    args = parser.parse_args()
    main(args)
