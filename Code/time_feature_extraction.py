import pandas as pd
import re
from datetime import datetime
from dateutil import tz

def timefeatures(time):
    '''Calculates the day(Sun to Sat), daynumber(0 to 6), hour (0 to 23),
    month and year from the time input

    input: 
        text: a date string with UTC time (example 2015-08-25T20:04:14+0000) 
    returns: 
        day (Tuesday), daynumber (2), hour (20), monthyear (082015)  ... [NewYorkTime]
    '''
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')

    [y,m,d,H,M,S]=re.search(r'(\d+)-(\d+)-(\d+)T(\d+):(\d+):(\d+)',time).group(1,2,3,4,5,6)
    utc = datetime(int(y), int(m), int(d), int(H), int(M), int(S))
    utc = utc.replace(tzinfo=from_zone)
    central = utc.astimezone(to_zone)
    day = central.strftime('%A')
    daynumber = central.strftime('%w')    
    monthyr  = m + y

    return day, daynumber, H, monthyr

##Load data 
data_pd_format = pd.read_csv('data_with_features.csv')

##calculate time features and store in the pandas data frame
data_pd_format['day'],data_pd_format['daynumber'],data_pd_format['hour'],data_pd_format['monthyear'] = zip(*data_pd_format['time'].map(timefeatures))

##Save to a CSV file
data_pd_format.to_csv('data_with_features.csv',index = False)