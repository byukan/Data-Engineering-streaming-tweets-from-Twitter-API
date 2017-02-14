import os
import yaml
from twitter import *
import pymongo

credentials = yaml.load(open(os.path.expanduser('~/api_cred.yml')))
creds = credentials['twitter']

client = pymongo.MongoClient('localhost', 27017)

db = client.twitter_db

twitter_stream = TwitterStream(auth=OAuth(creds.get('token'),
                       creds.get('token_secret'),
                       creds.get('consumer_key'),
                       creds.get('consumer_secret')))

iterator = twitter_stream.statuses.sample()

for tweet in iterator:
    db.tweets.insert_one(tweet)