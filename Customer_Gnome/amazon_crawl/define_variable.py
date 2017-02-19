product = "samsungj7"
platform_name = "amazon"
table_name = platform_name+'_'+product
import product
from product import views
#url_amazon = "http://www.amazon.in/Moto-3rd-Generation-Black-16GB/product-reviews/B013EIM5G6"
#url_amazon = "http://www.amazon.in/Sony-Xperia-C2104-Diamond-White/product-reviews/B00DF01AAG"
if platform_name == 'amazon':
	#url_amazon = "http://www.amazon.in/Moto-3rd-Generation-Black-16GB/product-reviews/B013EIM5G6"
	#url_amazon =  "http://www.amazon.in/Xiaomi-Mi-4-White-16GB/product-reviews/B00VEB0F22"
	print "after....."
	print views.resultt
	tmp = views.resultt
	print tmp[0]
	print '\n\n'
	print tmp[0].decode('utf-8')
	print "\n\n"
	print type(tmp[0].decode('utf-8'))
	url_amazon = str(tmp[0].decode('utf-8'))
	# url_amazon = "http://www.amazon.in/Apple-iPhone-5s-Silver-16GB/product-reviews/B00FXLCG7G"
elif platform_name == "snapdeal":
	url_snapdeal = "https://www.snapdeal.com/product/apple-iphone-5s-16-gb/1204769399/reviews"