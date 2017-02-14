#!/usr/bin/env python

"""
    @file twitter_firehose_kinesis.py

        set up firehose delivery stream http://docs.aws.amazon.com/firehose/latest/dev/basic-create.html#console-to

        ubuntu:
            sudo apt install awscli
            aws configure
            sudo pip install boto3
            nohup python twitter_firehose_kinesis.py&
"""

import json
import os

import boto3
import yaml
from twitter import TwitterStream, OAuth


def firehose_tweets(twitter_stream):
    """
    INPUT: twitter_stream object.
    OUTPUT: tweets in json format inserted in S3 using Kinesis.
    """
    iterator = twitter_stream.statuses.sample()
    for tweet in iterator:
        if 'id' in tweet:
            try:
                response = firehose_client.put_record(
                    DeliveryStreamName='twitter_firehose',
                    Record={'Data': json.dumps(tweet) + '\n'})
                # print(response)
            except Exception:
                print("Did not work.")


if __name__ == '__main__':

    credentials = yaml.load(open(os.path.expanduser('~/api_cred.yml')))
    firehose_client = boto3.client('firehose', region_name='us-east-1')
    twitter_stream = TwitterStream(auth=OAuth(**credentials['twitter']))

    while True:
        firehose_tweets(twitter_stream)
