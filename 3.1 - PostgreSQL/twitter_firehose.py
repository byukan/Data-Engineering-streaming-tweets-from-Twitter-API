#! /usr/bin/env python
# -*- coding: <utf-8> -*-

import os
import sys

import psycopg2
import yaml
from psycopg2.extras import Json
from twitter import TwitterStream, OAuth

# import pymongo
# # load twitter credentials
# credentials = yaml.load(open(os.path.expanduser('~/api_cred.yml')))
# token = credentials['twitter']['token']
# token_secret = credentials['twitter']['token_secret']
# consumer_key = credentials['twitter']['consumer_key']
# consumer_secret = credentials['twitter']['consumer_secret']

credentials = yaml.load(open(os.path.expanduser('~/api_cred.yml')))

creds = credentials['twitter']

# client = pymongo.MongoClient('localhost', 27017)

# db = client.twitter_db

twitter_stream = TwitterStream(auth=OAuth(creds.get('token'),
                                          creds.get('token_secret'),
                                          creds.get('consumer_key'),
                                          creds.get('consumer_secret')))

# load postgres credentials
pgcred = yaml.load(open(os.path.expanduser('~/postgres.yml')))['postgres']
dbname = pgcred['dbname']
user = pgcred['user']
password = pgcred['password']
host = pgcred['host']
port = pgcred['port']

if __name__ == '__main__':
    while True:
        # make connection
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
        # create cursor
        cursor = conn.cursor()
        # connect to twitter stream
        t = twitter_stream
        # sample tweets
        tweets = t.statuses.sample(encoding='utf-8')
        for tweet in tweets:
            # check for deletions
            if u'delete' in tweet.keys():
                continue
            else:
                # execute insertion
                cursor.execute('INSERT INTO raw_tweets (status) VALUES (%s)', [Json(tweet)])
                # cursor.execute("INSERT INTO raw_tweets (status) VALUES (%s)",
                #                [json.dumps(tweet, ensure_ascii=False).encode('utf8')])
                # commit change
                conn.commit()
        # close connection
        sys.stdout.write('!')
        conn.close()

# import os
# import yaml
# from twitter import *
# import pymongo
#
# credentials = yaml.load(open(os.path.expanduser('~/api_cred.yml')))
# creds = credentials['twitter']
#
# client = pymongo.MongoClient('localhost', 27017)
#
# db = client.twitter_db
#
# twitter_stream = TwitterStream(auth=OAuth(creds.get('token'),
#                        creds.get('token_secret'),
#                        creds.get('consumer_key'),
#                        creds.get('consumer_secret')))
#
# iterator = twitter_stream.statuses.sample()
#
# for tweet in iterator:
#     if 'delete' not in tweet.keys():
#         # print(tweet)
#         db.tweets.insert_one(tweet)
