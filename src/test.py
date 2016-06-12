import codecs
from latent_semantic_analyzer import MemoryFreeCorpus
from latent_semantic_analyzer import LatentSemanticAnalyzer
from gensim import corpora, models, similarities
import logging


# Set logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Initialize analyzer
lsa = LatentSemanticAnalyzer('twitterdata', 'cleanedteststream')

# Initialize Tf-Idf model using our corpus
tf_idf_model = models.TfidfModel(corpus=lsa.corpus)

# Apply Tf-Idf transformation to our corpus
tf_idf_corpus = tf_idf_model[lsa.corpus]

num_topics = 200

# Initialize LSI model using the Tf-Idf corpus
lsi_model = models.lsimodel.LsiModel(corpus=tf_idf_corpus, id2word=lsa.dictionary, num_topics=num_topics)

# Apply LSI transformation to the Tf-Idf corpus
lsi_corpus = lsi_model[tf_idf_corpus]

f = codecs.open('../topics.txt', 'w', 'utf-8')
for i in xrange(num_topics):
    topic = lsi_model.show_topic(i)
    for token in topic:
        f.write(token[0] + '|')
    f.write('\n')
f.close()

'''
tfidf = models.TfidfModel(corpus)
index = similarities.SparseMatrixSimilarity(tfidf[corpus])
vec = [(0, 1), (4, 1)]
sims = index[tfidf[vec]]
print(list(enumerate(sims)))
'''

'''
from tweet_cleaner import TweetCleaner
from pymongo import MongoClient

client = MongoClient()
db = client['twitterdata']
coll = db['teststream']

cursor = coll.find()
#tweet = cursor[0]['text']
#print tweet
tweet = u"@SomeHandle  I luv my &lt;3 iphone &amp; you're awsm apple. DisplayIsAwesome, sooo happppppy \uD800 http://www.apple.com"
tc = TweetCleaner()
cleaned_tweet = tc.clean(tweet)
print cleaned_tweet
'''