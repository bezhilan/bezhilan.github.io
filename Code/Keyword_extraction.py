''' Certain keywords show up highly frequently in the top 5% of the posts. 
So we wanted to explore the effect of these keywords'''

import pandas as pd
import re
import sys  
reload(sys) 
sys.setdefaultencoding('utf8')

def keyword_families(keylist, text):
    ''' Calculates the number of occurences of keywords belonging to a thematic family of words
    in the given text'''
    count = 0 
    for w in keylist:
        count = count + len(re.findall(w,text))

    return count

##Define the list of keywords relating to politics, women, crime, virality etc...
city = ['jersey','york','brookyln','manhattan','nyc','bronx']
politics = ['obama','bush','clinton','trump','cruz','carson','governor','senat']
women = ['woman','daughter','girl','mother','child','babi','mom','sister','pregnanc','teen','coupl','son']
majorcrime = ['dead','die','death','kill','shoot','polic','arrest','assasin','nypd','cop','shot','attack', 'blast','injur', 'rape','disturb','punish','bleed','shock','secur','bust']
minorcrime = ['suspect','alleg','charg','complaint','disturb','steal']
sex = ['sex','nude','strip','bed','bedroom']
year = ['year','month']
video = ['video']
viral = ['viral','break']
number = ['\d']

##Load data 
data_pd_format = pd.read_csv('data_with_features.csv')

##Find the number of occurences of keywords
data_pd_format['city'] = data_pd_format['processed_message'].map(lambda x: keyword_families(city, str(x)))
data_pd_format['politics'] = data_pd_format['processed_message'].map(lambda x: keyword_families(politics, str(x)))
data_pd_format['women'] = data_pd_format['processed_message'].map(lambda x: keyword_families(women, str(x)))
data_pd_format['majorcrime'] = data_pd_format['processed_message'].map(lambda x: keyword_families(majorcrime, str(x)))
data_pd_format['minorcrime'] = data_pd_format['processed_message'].map(lambda x: keyword_families(minorcrime, str(x)))
data_pd_format['sex'] = data_pd_format['processed_message'].map(lambda x: keyword_families(sex, str(x)))
data_pd_format['year'] = data_pd_format['processed_message'].map(lambda x: keyword_families(year, str(x)))
data_pd_format['video'] = data_pd_format['processed_message'].map(lambda x: keyword_families(video, str(x)))
data_pd_format['viral'] = data_pd_format['processed_message'].map(lambda x: keyword_families(viral, str(x)))
data_pd_format['number'] = data_pd_format['message'].map(lambda x: keyword_families(number, str(x)))

##Save to a CSV file
data_pd_format.to_csv('data_with_features.csv',index = False)

