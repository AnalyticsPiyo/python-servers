# -*- coding: utf-8 -*-

import tweepy
import sys

# 　ID、名前、ユニークID、ツイート、メディア、地理情報

CONSUMER_KEY        = '*****'
CONSUMER_SECRET     = '*****'
ACCESS_TOKEN_KEY    = '*****'
ACCESS_TOKEN_SECRET = '*****'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
query = '"*****"'
public_tweets = api.search(q=query, count = 50, lang='ja')
f = open('./test.txt', mode='a')
for tweet in public_tweets:
    try:
        print('tweet.text')
        print(tweet.text)
        print('tweet.user.id_str')
        print(tweet.user.id_str)
        print('tweet.user.name')
        print(tweet.user.name)
        print('tweet.user.description')
        print(tweet.user.description)
        print('tweet.user.location')
        print(tweet.user.location)
        print('tweet.geo')
        print(tweet.geo)
        print('media')
        tweet.extended_entities['media']
    except:
        pass
    print("------------------------------------------")

print('FINISH!!!')
f.close()
