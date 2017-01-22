import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['movie_analysis_db']
collection = db['movie_tweets']

with open('2point0-backup.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if line != '\n':
            tweet = json.loads(line)
            collection.insert(tweet)
            # print(tweet)