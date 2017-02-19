def main_snap():
	from scrape_snapdeal import Crawl
	from dbms_engine import DBMS
	import product
	from product import views
	import re
	#import define_variable
	#tbname = define_variable.table_name
	import product
	from product import views
	url = str(views.resultt[1].decode('utf-8'))
	tmp_name = url.split('/')
	name = re.sub('[^A-Za-z0-9]+', '_', tmp_name[4])
	# import define_variable
	# base_url = define_variable.url_snapdeal
	# platform = define_variable.platform_name
	# product = define_variable.table_name
	product = "snapdeal_" + name
	platform = "snapdeal"
	base_url = str(views.resultt[1].decode('utf-8')) + '/reviews'
	print "base url...."
	print base_url
	obj1 = DBMS(platform,product)
	print("no")
	if obj1.__check_create_table__():
		print("yes")
		obj2 = Crawl(base_url,platform,product)
		obj2.__scrape__()
	else:
		print('table already exist\n\n')
