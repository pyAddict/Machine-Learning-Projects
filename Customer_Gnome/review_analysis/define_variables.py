table1 = 'amazon_Apple_iPhone_5s_Silver_16GB'#used in training
table2 = "snapdeal_apple_iphone_5s_16_gb"#used in training
#table3 = "amazon_XiaomiMi4White16GB"#used in testing
#table4 = "snapdeal_XiaomiMi4White16GB"#used in testing
import re
import product
from product import views
url = str(views.resultt[0].decode('utf-8'))
tmp_name = url.split('/')
name = re.sub('[^A-Za-z0-9]+', '_', tmp_name[3])
product = name
platform_name = "amazon"
table_name = platform_name+'_'+product
tbname = table_name
table3 = tbname
print table3

url = str(views.resultt[1].decode('utf-8'))
tmp_name = url.split('/')
name = re.sub('[^A-Za-z0-9]+', '_', tmp_name[4])
platform_name = "snapdeal"
table_name = platform_name+'_'+name

table4 = table_name
print table4
# table3 = "amazon_SamsungGalaxyJ7SMJ700FGold"
# table4 = "snapdeal_samsungj716gbespressobrown"

