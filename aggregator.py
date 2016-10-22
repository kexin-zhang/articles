import newspaper
from newspaper import Article
import pymongo
from pymongo import MongoClient
from password import MONGO_USER, MONGO_PASS

connection = MongoClient("ds063536.mlab.com", port=63536)
db = connection['articles']
db.authenticate(MONGO_USER, MONGO_PASS)
collection = db['all_articles']

sources = [
	"http://www.cnn.com/",
	"http://www.nytimes.com/",
	"http://www.huffingtonpost.com/",
	"https://www.theguardian.com/",
	"http://www.foxnews.com/",
	"http://www.bbc.com/news",
	"https://www.yahoo.com/news/",
	"http://www.usatoday.com/",
	"https://www.theatlantic.com/",
	"https://www.washingtonpost.com/",
	"http://www.wsj.com/",
	"http://www.reuters.com/",
]

for source in sources: 
	paper = newspaper.build(source, memoize_articles=False)
	for article in paper.articles:
		article.download()
		article.parse()
		try:
			article.nlp()
			url = article.url
			authors = article.authors
			date = article.publish_date
			keywords = article.keywords
			text = article.text
			title = article.title
			if len(keywords) > 0:
				doc = {
						'date': date,
						'title': title,
						'keywords': keywords,
						'authors': authors, 
						'url': url,
					}
				collection.update_one({'title': title, 'authors': authors},
					{'$set': doc}, upsert=True)
				print title
		except Exception, e: 
			print str(e)



