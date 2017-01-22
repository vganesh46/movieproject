import tweepy
import sys
import jsonpickle
import os
from pymongo import MongoClient

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

searchQuery = '#GPSK'  # this is what we're searching for
maxTweets = 10000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = 'GautamiPutraSatakarni.txt' # We'll store the tweets in a text file.

client = MongoClient('localhost', 27017)
db = client['movie_analysis_db']
collection = db['movie_tweets']

# If results from a specific ID onwards are reqd, set since_id to that ID.
# else default to no lower limit, go as far back as API allows
sinceId = ''
cursor1 = db.movie_tweets.find({"entities.hashtags.text" : "GPSK"}).sort("id",-1).limit(1)
for record in cursor1:
    sinceId = record['id']
print(sinceId)
# If results only below a specific ID are, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1L

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
            collection.insert(tweet._json)
#                f.write(jsonpickle.encode(tweet._json, unpicklable=False) +
#                        '\n')
        tweetCount += len(new_tweets)
        print("Downloaded {0} tweets".format(tweetCount))
        max_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # Just exit if any error
        print("some error : " + str(e))
        break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))