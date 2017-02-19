from bs4 import BeautifulSoup as bsoup
import requests as rq
import re
from dbms_engine import DBMS
from pipelines import PutTodB
from connection import db
class Crawl():
	def __init__(self,url=None,platform=None,product=None):
		self.url = url
		self.platform = platform
		self.product = product

	def __scrape__(self):
		#obj3 = DBMS(self.platform,self.product)
		base_url = self.url
		r = rq.get(base_url)
		soup = bsoup(r.text)

		try: # Make sure there are more than one page, otherwise, set to 1.
		    a = soup.find_all('div',{'class':'pagination'})
		    aa = a[0].find_all('li')
		    num_pages = int(aa[4].get_text().strip('\n'))
		except IndexError:
		    num_pages = 1
		    
		print num_pages

		# Add 1 because Python range.
		url_list = ["{}?page={}".format(base_url, str(page)) for page in range(1, num_pages + 1)]

		for url_ in url_list:
		    print url_
		    r_new = rq.get(url_)
		    soup_new = bsoup(r_new.text)
		    try:
		       	b = soup_new.findAll('div',{'class':'commentreview'})
		        bb = b[0].findAll('div',{'class':'user-review'})
		        for i in bb:
		            review_raw = i.find_all('p')
		            review = review_raw[0].get_text().replace('\n','').replace('\t','').strip()
		            review = ''.join([x.encode('UTF8') for x in review])
		            details = i.find_all('div')
		            title = details[1].get_text().replace('\n','').replace('\t','').strip()
		            title = ''.join([x.encode('UTF8') for x in title])
		            txt = str(i.findAll('div',{'class':'rating'}))
		            rating = len(re.findall("sd-icon sd-icon-star active", txt))
		            record = PutTodB(title=title,rating=rating,review=review)
		            #print record
		            db.add(record)
		            db.commit()
		            
		    except Exception as e:
		        print e
		        pass
