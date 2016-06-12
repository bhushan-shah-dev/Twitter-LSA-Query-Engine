from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import HTMLParser
import unidecode
import re
import string
import itertools
from stop_words import get_stop_words

# Ref: http://www.analyticsvidhya.com/blog/2014/11/text-data-cleaning-steps-python/


class TweetCleaner:

    def clean(self, tweet):
        tweet = self.__escape_html_chars(tweet)
        tweet = self.__remove_RT(tweet)
        #tweet = self.__split_attached_words(tweet)
        tokenizer = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=True)
        tweet = ' '.join(tokenizer.tokenize(tweet))
        tweet = self.__clean_diacritics(tweet)
        #tweet = self.__remove_emojis(tweet)
        #tweet = self.__convert_unicode_to_str(tweet)
        tweet = self.__clean_apostrophes(tweet)
        tweet = self.__remove_hyperlinks(tweet)
        tweet = self.__remove_stop_words(tweet)
        tweet= self.__remove_punctuation(tweet)
        return tweet

    def __escape_html_chars(self, tweet):
        html_parser = HTMLParser.HTMLParser()
        return html_parser.unescape(tweet)

    def __clean_diacritics(self, tweet):
        return unidecode.unidecode(tweet)

    def __remove_emojis(self, tweet):
        # Ref: http://stackoverflow.com/questions/13729638/how-can-i-filter-emoji-characters-from-my-input-so-i-can-save-in-mysql-5-5
        try:
            # UCS-4
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            # UCS-2
            highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
        return highpoints.sub(u'', tweet)

    def __remove_RT(self, tweet):
        return re.sub('RT ', '', tweet)

    def __clean_apostrophes(self, tweet):
        # Example: Convert "Jordan's" into "Jordan", since we do not know if the "'s" indicates possession or is short for "is", which would be anyway removed when we remove stop words
        # Example: Similarly, convert "you're" into "you", "they're" into "they" etc, since "are" would also be removed when we remove stop words
        return re.sub('\'(s|re) ', ' ', tweet)

    def __remove_hyperlinks(self, tweet):
        url_regex = ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))'
        # Regex source: https://gist.github.com/uogbuji/705383
        return re.sub(url_regex, '', tweet)

    def __remove_stop_words(self, tweet):
        cached_stop_words = stopwords.words("english")
        return ' '.join([word for word in tweet.split() if word not in cached_stop_words])

    def __remove_punctuation(self, tweet):
        punctuation_except_hash = string.punctuation.translate(None,"#")
        tweet = tweet.translate(None, punctuation_except_hash)
        # TODO: Handle cases like decimal points, hyphens within words/names
        return tweet

    def __split_attached_words(self, tweet):
        tweet = " ".join(re.findall('[A-Z][^A-Z]*', tweet))
        return tweet

