''' Read through the datafile (list of post JSONs) and exports the variables of interest to a Pandas dataframe'''

import pandas as pd
import json
import sys  
reload(sys) 
sys.setdefaultencoding('utf8')

##Load data
pix_posts = []
with open('../data/post/pix_posts_year.json', 'r') as f:
    for line in f:
        pix_posts.append(json.loads(line))

##Create a list of relevant data
data = []

for post in pix_posts:

    post_id = post.get('id', '')
    time = post.get('created_time', '')

##Content of the status message
    message = post.get('message', '')

##The number of people your advertised Page post was served to. (Unique Users)
    paid  = post['insights']['post_impressions_paid_unique']['values'][0]['value']   

## engagement = The sum of post clicks, post likes, post comments and post shares.         
    engagement = post['insights'].get('net_engaged_users', '')

##The total number of people your Page post was served to. (Unique Users)
    reach = post['insights']['post_impressions_unique']['values'][0]['value']

## The number of clicks on the link (item being shared)
    try:
        link_clicks = post['insights']['post_consumptions_by_type']['values'][0]['value']['link clicks']
    except:
        link_clicks = 0

    output = [time, post_id, message, engagement, reach, link_clicks, paid]
    data.append(output)

#convert list to pandas format
data_pd_format = pd.DataFrame(data, columns= ['time', 'post_id', 'message', 'engagement', 'reach', 'link_clicks', 'paid'])

## Remove paid posts
data_pd_format = data_pd_format[data_pd_format.paid == 0]

## Remove posts will < 100 reach
data_pd_format = data_pd_format[data_pd_format.reach > 100]

##Calculate ratios
data_pd_format['engagement_to_reach'] = data_pd_format['engagement']/data_pd_format['reach']
data_pd_format['link_to_reach'] = data_pd_format['link_clicks']/data_pd_format['reach']

#create buckets based on a median split 
# 0 for low and 1 for high
data_pd_format['engagement_to_reach_buckets'] = pd.qcut(data_pd_format.engagement_to_reach,2,labels =['0','1'])
data_pd_format['engagement_buckets'] = pd.qcut(data_pd_format.engagement,2,labels =['0','1'])
data_pd_format['link_buckets'] = pd.qcut(data_pd_format.link_clicks,2,labels =['0','1'])
data_pd_format['link_to_reach_buckets'] = pd.qcut(data_pd_format.link_to_reach,2,labels =['0','1'])

#Save to a CSV file
data_pd_format.to_csv('data_from_json.csv',index = False)

