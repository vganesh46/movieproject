import tweepy
from tweepy import OAuthHandler
from tweepy.parsers import JSONParser
import json
import time

consumer_key = 'GrUmb0gEqnyF3GIFXSr0l9mXX'
consumer_secret = '6GSKBGdNm7V18GjWmOEX8VHA0N7AMYkVRonWvU9BryYqmVTmAF'
access_token = '4714359180-4TNaNM2fuJLtrtsMrUaZDvuMQb4VsEk1QSBsGK5'
access_secret = 'BRFk5QEgOKTl1O7yfRtdZkKjJMhLL1RVRuCRKqgd4clEt'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

tweets = tweepy.Cursor(api.search, q='#2point0',).items(10000)
statuses = []
def jdefault(o):
    return o.__dict__
    
with open('2point0.json', 'w') as outfile:
    
    while True:
        try:
            tweet = tweets.next()
            data = {}
            data['text'] = tweet._json['text']
            print tweet._json['text']
            json_data = json.dumps(data, separators=(',', ':'))
            outfile.write(json_data + '\n')
        except tweepy.TweepError:
            time.sleep(60 * 15)
            continue
        except StopIteration:
            break