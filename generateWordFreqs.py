import pymongo
from pymongo import MongoClient
from datetime import datetime
from password import MONGO_USER, MONGO_PASS
from itertools import combinations
import json

connection = MongoClient("ds063536.mlab.com", port=63536)
db = connection['articles']
db.authenticate(MONGO_USER, MONGO_PASS)
collection = db['all_articles']
count = collection.find({}).count()

pipeline = [
	{'$match': {'date': {'$gte': datetime(2016, 10, 15)}}},
	{'$unwind': '$keywords'},
	{'$group': {'_id': '$keywords', 'count': {'$sum': 1 }}},
	{'$sort': {'count': -1}},
	{'$limit': 15}
]

words = collection.aggregate(pipeline)
words = [str(word["_id"]) for word in list(words) if len(word["_id"]) > 3]
print words

output = sum([map(list, combinations(words, i)) for i in range(len(words) + 1)], [])

print output

toSave = []
for wordList in output:
	if len(wordList) > 0: 

		query = {'date': {'$gte': datetime(2016, 10, 15)}, 'keywords':{'$all': wordList}}
		combCount = collection.find(query).count()

		toSave.append({'sets': wordList, 'size': combCount})

with open("counts.json", 'w') as out:
	json.dump(toSave, out)