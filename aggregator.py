import newspaper
from newspaper import Article
import pymongo
from pymongo import MongoClient

connection = MongoClient()
db = connection['articles']
collection = db['article_data']

sources = [
	"http://www.cnn.com/",
	"http://www.nytimes.com/",
	"http://www.huffingtonpost.com/",
	"https://www.theguardian.com/",
	"https://www.news.yahoo.com/",
	"http://www.foxnews.com/",
	"http://www.forbes.com/",
	"http://www.bbc.com/news",
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
						'text': text,
						'url': url,
					}
				collection.update_one({'title': title, 'authors': authors},
					{'$set': doc}, upsert=True)
				print title
		except Exception, e: 
			print str(e)



