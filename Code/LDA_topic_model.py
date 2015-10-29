import pandas as pd
import numpy as np
from gensim import corpora, models, similarities
import gensim.parsing.preprocessing as preprocess
import gensim.matutils as mat
import pyLDAvis.gensim
import sys  
reload(sys) 
sys.setdefaultencoding('utf8')

def topicmodel(messagelist, idlist, stoplist, numberoftopics, agencyname):
	''' Given a list of processed messages and  postids for news agency 'agencyname', 
	this function removes the stop words,
	and performs topic modeling using Latent Dirichlet Allocation
	and finds 'numberoftopics' topic clusters
	The correponding topic distributions, visualization and LDA model is saved to the folder
	'''

##Make a list of words after removing the stopwords
	wordlist = [[word for word in str(document).split() if word not in stoplist] for document in messagelist]

## Create the dictionary and Corpus
	dictionary = corpora.Dictionary(wordlist)
	corpus = [dictionary.doc2bow(text) for text in wordlist]

## Now build the LDA model 
	lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=numberoftopics, update_every=1, chunksize=100, passes=1,gamma_threshold=0.001, minimum_probability=0.01, alpha = 'asymmetric')

## Save LDA model
	lda.save(agencyname + 'lda')

## LDA gives each topic as a distribution over words and each post/message as a mixture of topics
## LDA inference gives each document/post as a mixture of topics
	
	classify = lda.inference(corpus)[0]

##Create the column names as topic1, topic2 ..... topic'n'
	columnnames = []
	for i in np.arange(numberoftopics):
		columnnames.append('topic' + str(i+1))

##converted posts that are classified as a mixture of topics into a pandas dataframe		
	pd_classify = pd.DataFrame()
	pd_classify = pd.DataFrame(classify,columns = columnnames)

##add postIDs to the dataframe 
	pd_classify['post_id'] = idlist
	pd_classify['processed_message'] = messagelist

##Save to a CSV file
	topic_file_name = agencyname + '_post_topics.csv'
	pd_classify.to_csv(topic_file_name,index = False)

## Let's now do some cool visualizations using the pyLDAvis package
	data_created_using_prepare = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
	pyLDAvis.save_html(data_created_using_prepare,agencyname + str(numberoftopics) + 'topics_LDA.html')

	return

##Load data 
data_pd_format = pd.read_csv('data_with_features.csv')

## Stopwords: List of really high and low frequency words and other words which are known not to influence the topic model.
## Note: The processed message already have the usual stopwords removed see text_feature_extraction.py
stoplist = ['pix','pixcast','year','video','photo','news','directv','newsmax']

## Perform topic modeling for 'agency1's' data set
topicmodel(data_pd_format.processed_message,data_pd_format.post_id,stoplist,8,'pix')