from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client['movie_analysis_db']
collection = db['movie_tweets']

cursor = collection.aggregate(
    [
        {"$group": {"_id": "$id", "unique_ids": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
        {"$match": {"count": { "$gte": 2 }}}
    ]
)

response = []
for doc in cursor:
    del doc["unique_ids"][0]
    for id in doc["unique_ids"]:
        response.append(id)

collection.remove({"_id": {"$in": response}})