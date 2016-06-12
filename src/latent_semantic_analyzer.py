from __future__ import division
from pymongo import MongoClient
from gensim import corpora, models, similarities
from stop_words import get_stop_words
from tweet_cleaner import TweetCleaner


'''
Ref: http://blog.josephwilk.net/projects/latent-semantic-analysis-in-python.html
'''


class MemoryFreeCorpus:

    def __init__(self, dictionary, database, collection, host='localhost', port=27017):
        self.host = host
        self.port = port
        self.database = database
        self.collection = collection
        self.dictionary = dictionary

    def __iter__(self):
        client = MongoClient(host=self.host, port=self.port)
        db = client[self.database]
        coll = db[self.collection]

        cursor = coll.find()

        for doc in cursor:
            yield self.dictionary.doc2bow(doc['text'].split())


class LatentSemanticAnalyzer:

    def __init__(self, database, collection, host='localhost', port=27017):
        self.host = host
        self.port = port
        self.database = database
        self.collection = collection
        self.dictionary = self.__create_dictionary()
        self.corpus = self.__create_corpus()

    def __create_corpus(self):
        if self.dictionary is None:
            raise ValueError("Dictionary not yet created...")
        corpus = MemoryFreeCorpus(self.dictionary, self.database, self.collection, self.host, self.port)
        return corpus

    def __create_dictionary(self):
        client = MongoClient(host=self.host, port=self.port)
        db = client[self.database]
        coll = db[self.collection]

        cursor = coll.find()

        # Add all words contained in all cleaned tweets
        dictionary = corpora.Dictionary(doc['text'].split() for doc in cursor)

        return dictionary

    '''
    def create_term_document_matrix(self):

        client = MongoClient(host=self.host, port=self.port)
        db = client[self.database]
        coll = db[self.collection]

        cursor = coll.find()

        tweet_list = []
        for doc in cursor:
            tweet_text = doc['text']
            tweet_list.append(tweet_text)

        count_vectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
        term_document_matrix = count_vectorizer.fit_transform(tweet_list)

        self.matrix = term_document_matrix

    def svd(self):
        if self.matrix is None:
            raise ValueError('Term document matrix not created yet...')
        self.u, self.sigma, self.vt = sparsesvd(self.matrix)
    '''