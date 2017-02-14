#!/usr/bin/env python
<<<<<<< HEAD
import json
import sys

# input comes from STDIN (standard input)
# hashtags_list = []
for line in sys.stdin:
    try:
        tweet = json.loads(line)
        entity = tweet['entities']
        # assert isinstance(entity, object)
        if entity is not None and (entity['hashtags'] is not None or len(entity['hashtags']) != 0):
            for hashtags in entity['hashtags']:
                print '%s 1' % (hashtags['text'].lower())

    except:
        pass
=======

import json
import sys

for line in sys.stdin:
    line = line.strip()
    tweet = json.loads(line)
    entities = tweet.get('entities')
    if entities:
        for hashtag in entities.get('hashtags', []):
            try:
                print '%s\t%s' % (hashtag.get('text'), 1)
            except UnicodeEncodeError:
                pass
>>>>>>> zipfian/master
