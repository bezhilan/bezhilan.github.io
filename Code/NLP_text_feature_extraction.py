''' We use NLP tools to process the message text, extract text features like keywords, post length, 
    number of ALL CAPS words at the start of the message, and time features'''

import pandas as pd
import re
import nltk
import sys

from gensim import corpora, models, similarities
import gensim.parsing.preprocessing as preprocess
import gensim.matutils as mat
from nltk.stem import *

from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer

#stemmer = PorterStemmer()
stemmer = SnowballStemmer("english")

reload(sys) 
sys.setdefaultencoding('utf8')
sys.path.append('/Users/Barath/anaconda/lib/python2.7/site-packages')


##Load data from data_from_json
data_pd_format = pd.read_csv('data_from_json.csv')


def preprocessing(text):
    '''Preprocesses a text using standard gensim techniques: 
    removes stopwords, strips short words (1-2 characters), strips numbers, 
    strips http addresses, strips Unicode from emoji etc., lowercases everything, 
    strips extra spaces, punctuation, non-alphanumeric symbols. Also perform stemming

    input: 
        text: a string
    returns: 
        the preprocessed string.
    '''
    text = text.lower()
    text = preprocess.remove_stopwords(text) # remove stop words
    text = preprocess.strip_short(text) #get rid of short words
    text = preprocess.strip_numeric(text) #get rid of numbers
    p = re.compile(r'(http.*\s)|(http.*$)')
    text = p.sub('',text)
    p = re.compile(r'[^\x00-\x7F]+')
    text = p.sub('',text)
    text = preprocess.strip_multiple_whitespaces(text)
    text = preprocess.strip_punctuation(text)
    text = preprocess.strip_non_alphanum(text)
    text = preprocess.remove_stopwords(text)
    text = preprocess.strip_short(text)
# stemming
    words = text.split()
    stemmed_words = [stemmer.stem(word) for word in words]
    text = ' '.join(stemmed_words)

    return text

def wordcount(text):
    '''Calculate post length after removing http addresses, 
       numbers and multiple whitespaces

    input: 
        text: a string
    returns: 
        the adjusted wordcount.
    '''
    text = preprocess.strip_numeric(text) #get rid of numbers
    p = re.compile(r'(http.*\s)|(http.*$)')
    text = p.sub('',text)
    p = re.compile(r'[^\x00-\x7F]+')
    text = p.sub('',text)
    text = preprocess.strip_multiple_whitespaces(text)
    words = text.split()
    count = len(words)
    return count


def ALLCAPS(text):
    '''Calculates the number of ALL CAPS words at the start of the message
     after removing http addresses, numbers and multiple whitespaces

    input: 
        text: a string
    returns: 
        the number of ALL CAPS words at the start of the message
    '''
    text = preprocess.strip_numeric(text) #get rid of numbers
    p = re.compile(r'(http.*\s)|(http.*$)')
    text = p.sub('',text)
    p = re.compile(r'[^\x00-\x7F]+')
    text = p.sub('',text)
    text = preprocess.strip_multiple_whitespaces(text)
    words = text.split()
    ALLCAPScount = 0

    for w in words:
        if w.isupper() == False:
            break
        ALLCAPScount = ALLCAPScount + 1

    if ALLCAPScount:    
        if (words[ALLCAPScount-1] == 'A'):    
            ALLCAPScount = ALLCAPScount - 1

    return ALLCAPScount

#get word count, ALL CAPS and processed message

data_pd_format['word_count'] = [wordcount(str(text)) for text in data_pd_format.message]
data_pd_format['ALLCAPS'] = [ALLCAPS(str(text)) for text in data_pd_format.message]
data_pd_format['processed_message'] = [preprocessing(str(text)) for text in data_pd_format.message]

##Save to a CSV file
data_pd_format.to_csv('data_with_features.csv',index = False)
