import tweepy
import sys
import jsonpickle
import os
import json
import pymongo
from pymongo import MongoClient

def get_tweet_id(line):
    '''
    Extracts and returns tweet ID from a line in the input.
    '''
    (tagid,_timestamp,_sandyflag) = line.split('\t')
    (_tag, _search, tweet_id) = tagid.split(':')
    return tweet_id

API_KEY = 'GrUmb0gEqnyF3GIFXSr0l9mXX'
API_SECRET = '6GSKBGdNm7V18GjWmOEX8VHA0N7AMYkVRonWvU9BryYqmVTmAF'
# Replace the API_KEY and API_SECRET with your application's key and secret.
auth = tweepy.AppAuthHandler(API_KEY, API_SECRET)
 
api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)
 
if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)
 
# Continue with rest of code
client = MongoClient('localhost', 27017)
db = client['movie_analysis_db']
# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.


moviecursor = db.movie_info.find({"isActive" : 1})
for movierecord in moviecursor:
    max_id = -1L
    print ("Started downloading tweets for {0} ".format(movierecord['name']))
    searchQuery = movierecord['tags']  # this is what we're searching for
    maxTweets = 10000000 # Some arbitrary large number
    tweetsPerQry = 100  # this is the max the API permits
    movie_max_id = -1
    
    collection = db['movie_tweets']

    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = ''
    if (movierecord['max_id'] >= 0):
        sinceId = movierecord['max_id']
    print(sinceId) 

    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    # with open(fName, 'r') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                try:
                    collection.insert(tweet._json)
                except pymongo.errors.DuplicateKeyError as e:
                    print("Duplicate tweet : " + str(e))
            if( tweet.id > movie_max_id):
                movie_max_id = tweet.id
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break
    if (max_id >= -1):          
        print("Max Id : {0}".format(movie_max_id))
        db.movie_info.update({ "name": movierecord['name']},{"$set": {"max_id": movie_max_id}})
    print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, movierecord['name']))
    
    
