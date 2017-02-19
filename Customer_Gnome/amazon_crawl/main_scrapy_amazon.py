def main_scrapy():
	from scrapy.crawler import CrawlerProcess
	from scrapy_amazon import MySpider
	from connection import engine
	from sqlalchemy import Column, String, Integer, DateTime, MetaData,Table
	import re
	#import define_variable
	#tbname = define_variable.table_name
	import product
	from product import views
	url = str(views.resultt[0].decode('utf-8'))
	tmp_name = url.split('/')
	name = re.sub('[^A-Za-z0-9]+', '_', tmp_name[3])
	product = name
	platform_name = "amazon"
	table_name = platform_name+'_'+product
	tbname = table_name
	print("no")
	if not engine.dialect.has_table(engine,tbname):
		print("yes")
		metadata = MetaData(engine)
		Table(tbname, metadata,Column('Id',Integer, primary_key=True),Column('title', String(1000)), Column('rating', Integer), Column('upvotes', Integer),
			Column('review', String(100000)))
		metadata.create_all()
		#process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)','FEED_FORMAT': 'json','FEED_URI': 'result.json'})
		process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})

		process.crawl(MySpider)
		process.start()
	else:
		print('Table already exist\n')

	