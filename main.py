from flask import Flask, render_template, request, redirect, url_for
import pymongo
from pymongo import MongoClient
from datetime import datetime
import json
from password import MONGO_USER, MONGO_PASS

app = Flask(__name__)

@app.route('/')
def main():
    connection = MongoClient("ds063536.mlab.com", port=63536)
    db = connection['articles']
    db.authenticate(MONGO_USER, MONGO_PASS)
    collection = db['all_articles']
    count = collection.find({}).count()

    search = ['trump', 'clinton', 'state', 'york', 'states', 'united', 'world', '2016']
    or_pipeline = []
    for part in search:
        or_pipeline.append({'keywords': part})

    pipeline2 = [
        {'$match': {'$or': or_pipeline, 'date': {'$gte': datetime(2016, 10, 22), '$lte': datetime(2016, 10, 30)}}},
        {'$unwind': '$keywords'},
        {'$match': {'keywords': {'$in': search}}},
        {'$group': {'_id': {'keyword':'$keywords', 'date':'$date'}, 'count': {'$sum': 1 }}},
        {'$sort': {'count': -1}},
    ]

    words = collection.aggregate(pipeline2)
    x = {}
    for word in words:
        date = word['_id']['date'].strftime("%Y-%m-%d")
        key = word['_id']['keyword']
        if key in x:
            if date in x[key]:
                x[key][date] += int(word['count'])
            else:
                x[key][date] = int(word['count'])
        else:
            x[key] = {date: int(word['count'])}
    
    trends = [[], [], [], [], [], [], [], []]

    for item in x: 
        index = search.index(item)
        trends[index].extend([{'date': k, 'value': x[item][k]} for k in x[item]])

    return render_template('index.html', count = count, trends=json.dumps(trends))


@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    if len(query.strip()) > 0:
        return redirect(url_for('results', query=query)) 
    return redirect(url_for('main'))


@app.route('/results/<query>')
def results(query):
    connection = MongoClient("ds063536.mlab.com", port=63536)
    db = connection['articles']
    db.authenticate(MONGO_USER, MONGO_PASS)
    collection = db['all_articles']

    query = query.strip()
    or_pipeline = []
    for part in query.split():
        or_pipeline.append({'keywords': part})
        or_pipeline.append({'title': {'$regex': part,  "$options": "-i"}})
    #print or_pipeline

    pipeline = [
        {'$match': {'$or': or_pipeline, 'date': {'$gte': datetime(2016, 10, 22)}} },
        {'$group': {'_id': '$date','articles': {'$push': {'title': '$title', 'url': '$url', 'author': '$authors', 'keywords': '$keywords'} }}},
        {'$sort': {'_id': 1}}
    ]


    articles = collection.aggregate(pipeline)

    articles_length = {}
    all_articles = {}

    for article in articles:
        date = article['_id'].strftime("%Y-%m-%d")
        if date in all_articles:
            all_articles[date].extend(article['articles'])
            articles_length[date] = articles_length[date] + len(article['articles'])
        else:
            all_articles[date] = article['articles']
            articles_length[date] = len(article['articles'])

    if len(articles_length) > 0:            
        curr = datetime.now().strftime("%Y-%m-%d")
        if curr not in articles_length:
            articles_length[curr] = 0

    # pipeline2 = [
    #   {'$match': {'$or': or_pipeline, 'date': {'$gte': datetime(2016, 10, 15)}}},
    #   {'$unwind': '$keywords'},
    #   {'$group': {'_id': None, 'words': {'$push': {'word': '$keywords'}}}}
    # ]

    pipeline2 = [
        {'$match': {'$or': or_pipeline, 'date': {'$gte': datetime(2016, 10, 15)}}},
        {'$unwind': '$keywords'},
        {'$group': {'_id': '$keywords', 'count': {'$sum': 1 }}},
        {'$sort': {'count': -1}}
    ]

    words = collection.aggregate(pipeline2)

    # try:
    #   all_keywords = [item['word'] for item in list(words)[0]['words']]
    # except:
    #   all_keywords = []

    ignore = ['10000', 'hello']
    words_dict = {}
    for keyword in words:
        key = str(keyword["_id"])
        if query not in key and len(key) > 3 and key not in ignore:
            words_dict[key] = int(keyword["count"])
    #words_dict = {str(x["_id"]):int(x["count"]) for x in all_keywords if query not in str(x["_id"]) and len(str(x["_id"])) > 3 and str(x["_id"]) not in ignore }

    all_articles = json.dumps(all_articles)
    return render_template('search.html', articles=all_articles, keywords=words_dict, lengths = articles_length, query=query)

@app.route('/counts', methods=['GET'])
def count():
    with open("counts.json") as f:
        return f.read()

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500

if __name__ == "__main__":
   app.run(debug=True)

