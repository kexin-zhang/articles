import newspaper
from newspaper import Article
import unicodecsv as csv

sources = [
	'http://www.reuters.com/',
	'http://hosted.ap.org/',
	'http://www.npr.org/',
	'http://america.aljazeera.com/',
]

file = open('articles.csv', 'a')
writer = csv.writer(file, delimiter = ',')

for source in sources: 
	paper = newspaper.build(source)
	for article in paper.articles:
		article.download()
		article.parse()
		article.nlp()
		url = article.url
		authors = article.authors
		date = article.publish_date
		keywords = article.keywords
		text = article.text
		title = article.title
		print title
		writer.writerow((str(date), url, title, authors, keywords, text))
		file.flush()

file.close()

