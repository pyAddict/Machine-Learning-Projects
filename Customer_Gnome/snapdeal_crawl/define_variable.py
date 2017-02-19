product = "appleiphone5s16gb"
platform_name = "snapdeal"
table_name = platform_name+'_'+product
#url_amazon = "http://www.amazon.in/Moto-3rd-Generation-Black-16GB/product-reviews/B013EIM5G6"
#url_amazon = "http://www.amazon.in/Sony-Xperia-C2104-Diamond-White/product-reviews/B00DF01AAG"
if platform_name == 'amazon':
	url_amazon =  "http://www.amazon.in/Xiaomi-Mi-4-White-16GB/product-reviews/B00VEB0F22"
elif platform_name == "snapdeal":
	#url_snapdeal = "https://www.snapdeal.com/product/xiaomi-mi4-16-gb/634950686113/reviews"
	#url_snapdeal = "https://www.snapdeal.com/product/samsung-j7-16gb-espresso-brown/661359071561/reviews"
					#https://www.snapdeal.com/product/samsung-j7-16gb-espresso-brown/661359071561?page=1
	url_snapdeal = "https://www.snapdeal.com/product/apple-iphone-5s-16-gb/347830397/reviews"
