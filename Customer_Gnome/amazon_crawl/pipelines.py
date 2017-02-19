from sqlalchemy import Column, String, Integer, DateTime
from connection import Base,engine
import product
from product import views
import re
#import define_variable 
class PutTodB(Base):
    #platform = define_variable.platform_name
    #product = define_variable.table_name
    platform = 'amazon'
    url = str(views.resultt[0].decode('utf-8'))
    tmp_name = url.split('/')
    name = re.sub('[^A-Za-z0-9]+', '_', tmp_name[3])
    __tablename__ = "amazon_" + name
    Id = Column(Integer, primary_key=True)
    title = Column(String(1000))
    rating = Column(Integer)
    review = Column(String(100000))
    if platform == 'amazon':
        upvotes = Column(Integer)

    def __init__(self, Id=None,title=None, rating=None, upvotes=None, review=None):
        self.Id = Id
        self.title = title
        self.rating = rating
        self.upvotes = upvotes
        self.review = review

    def __repr__(self):
        if platform == 'amazon':
            return "<AllData: Id='%d',title='%s', rating='%d', upvotes='%d', review='%s'>" % (self.Id,self.title, self.rating, self.upvotes, self.review)
        elif platform == 'snapdeal':
            return "<AllData: title='%s', rating='%d', review='%s'>" % (self.title, self.rating, self.review)
# import pymongo

# from scrapy.exceptions import DropItem
# from scrapy import log

# settings = {'MONGODB_SERVER':"localhost","MONGODB_PORT":27017,"MONGODB_DB":"amazon","MONGODB_COLLECTION":"reviews"}

# class MongoDBPipeline(object):

#     def __init__(self):
#         connection = pymongo.MongoClient(
#             settings['MONGODB_SERVER'],
#             settings['MONGODB_PORT']
#         )
#         db = connection[settings['MONGODB_DB']]
#         self.collection = db[settings['MONGODB_COLLECTION']]

#     def process_item(self, item, spider):
#         valid = True
#         for data in item:
#             if not data:
#                 valid = False
#                 raise DropItem("Missing {0}!".format(data))
#         if valid:
#             self.collection.insert(dict(item))
#             log.msg("Review added to db",
#                     level=log.DEBUG, spider=spider)
#         return item