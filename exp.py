"""
Spyder Editor
This is a temporary script file.
"""

import tweepy
consumer_key = "XXXXXXXXXXXXXXXXXXXXX"
consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx"
access_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXx"
access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
name = "realDonaldTrump"
# Number of tweets to pull
tweetCount = 1

results = api.user_timeline(id=name, count=tweetCount)

for tweet in results:
   print (tweet.text)