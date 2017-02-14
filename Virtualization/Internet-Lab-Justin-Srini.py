
# coding: utf-8

# In[1]:

# https://github.com/justwjr/DSCI6007-student/blob/master/The%20Internet/lab.md
import os
import yaml
credentials = yaml.load(open(os.path.expanduser('~/api_cred.yml')))


# In[2]:

credentials


# In[3]:

credentials['twitter'].get('consumer_key')


# In[4]:

# https://github.com/ideoforms/python-twitter-examples/blob/master/twitter-trends.py


# In[5]:

#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-trends
#  - lists the current global trending topics
#-----------------------------------------------------------------------

from twitter import *

#-----------------------------------------------------------------------
# load our API credentials 
#-----------------------------------------------------------------------
# config = {}
# execfile("config.py", config)

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(auth = OAuth(credentials['twitter'].get('token'),
                               credentials['twitter'].get('token_secret'),
                               credentials['twitter'].get('consumer_key'), 
                               credentials['twitter'].get('consumer_secret'))
)

twitter


# In[6]:

#-----------------------------------------------------------------------
# retrieve global trends.
# other localised trends can be specified by looking up WOE IDs:
#   http://developer.yahoo.com/geo/geoplanet/
# twitter API docs: https://dev.twitter.com/docs/api/1/get/trends/%3Awoeid
#-----------------------------------------------------------------------
results = twitter.trends.place(_id = 23424977)

print "US Trends"

for location in results:
    for trend in location["trends"]:
        print " - %s" % trend["name"]


# In[7]:

trends = [trend["name"] for trend in location["trends"] for location in results]
trends[:10]


# In[8]:

import pandas as pd
df = pd.DataFrame(trends[:10])
df.head()


# In[14]:

top10html = df.to_html()
top10html


# In[16]:

myfile = open('top10.html', 'w')
myfile.write(top10html)
# for location in results:
#     for i, trend in enumerate(location["trends"]):
#         if i < 10:
#             myfile.write("%s\n" %trend["name"])
myfile.close()


# In[10]:

myfile = open('top10.txt', 'w')
for location in results:
    for i, trend in enumerate(location["trends"]):
        if i < 10:
            myfile.write("%s\n" %trend["name"])
myfile.close()


# In[11]:

ls


# In[12]:

import time
import boto
from boto.s3.connection import Location

#
# create a couple of strings with our very minimal web content
#
index_html = "<html><head><title>My Top Twitter Trends</title></head><body>"+ top10html +"</body></html>"

error_html = """
<html>
  <head><title>Something is wrong</title></head>
  <body><h2>Something is terribly wrong with my S3-based website</h2></body>
</html>"""

# create a connection to S3
conn = boto.connect_s3(host='s3-us-west-1.amazonaws.com')
# create a bucket and make it publicly readable
# website_bucket = conn.create_bucket('justw150',
#                                     location=Location.USWest,
#                                     policy='public-read')
website_bucket = conn.get_bucket('justw150')

# upload our HTML pages and make sure they are publicly readable
# also make sure Content-Type is set to text/html
index_key = website_bucket.new_key('index.html')
index_key.content_type = 'text/html'
index_key.set_contents_from_string(index_html, policy='public-read')
error_key = website_bucket.new_key('error.html')
error_key.content_type = 'text/html'
error_key.set_contents_from_string(error_html, policy='public-read')

# now set the website configuration for our bucket
website_bucket.configure_website('index.html', 'error.html')

time.sleep(5)

# now get the website configuration, just to check it
print website_bucket.get_website_configuration()


# In[13]:

# http://justw150.s3-website-us-west-1.amazonaws.com/


# In[ ]:



