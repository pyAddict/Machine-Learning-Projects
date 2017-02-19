from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
import re as r
from pipelines import PutTodB
from connection import db
from scrapy.item import Item, Field
#import define_variable
import product
from product import views
class Define_var(Item):
    title = Field()
    rating = Field() 
    upvotes = Field()
    review = Field()

class MySpider(CrawlSpider):
    name = "amazon"
    allowed_domains = ["www.amazon.in"]
    #start_urls = [define_variable.url_amazon]
    base_url = str(views.resultt[0].decode('utf-8')).replace('/dp/','/product-reviews/')
    print 'base_url_for amazon----\n\n'
    print base_url
    start_urls = [base_url]
    rules = (Rule(LinkExtractor(allow=('/ref=\w+(arp|getr)\w+\d+\?\ie=UTF8&pageNumber\=\d+\s?(&pageSize=10)?$',)), callback="_crawl_items", follow= True),)
    #rules = (Rule(LinkExtractor(allow=('/ref=cm_cr_arp_d_paging_btm_\d+\?\ie=UTF8&pageNumber\=\d+\s?(&pageSize=10)?$',)), callback="_crawl_items", follow= True),)
    def parse_start_url(self, response):
        return self._crawl_items(response)
        
    def _crawl_items(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath('//div[@class="a-section review"]')
        #all_info = []
        for i in titles:
            item=Define_var()

            item["title"]=(i.xpath("div[@class='a-row']//text()").extract())[1];

            tmp1=(i.re('(\d+\ (people))'))
            if(tmp1):
                tmp2=(r.search(r.compile('(\d+)'),str(tmp1))).group()
                item["upvotes"]=tmp2
            else:
                item["upvotes"]=0

            item["rating"]=(i.xpath("div[@class='a-row']//text()"))[0].re('(\d\.\d+)');

            item["review"]=i.xpath("div[@class='a-row review-data']//text()").extract()

            #all_info.append(item)
            #item = MongoDBPipeline().process_item(item, CrawlSpider)
            #yield item
            review_str = ''.join([x.encode('UTF8') for x in item['review']])#to make string from array
            print(review_str,'\n\n')
            record = PutTodB(title=item['title'],
                             rating=item['rating'],upvotes=item['upvotes'],
                             review=review_str)
            print("record")
            db.add(record)
            db.commit()
            yield item
        #return(all_info)

    
            
            

