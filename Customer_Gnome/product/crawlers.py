class Crawler():
    def __init__(self):
        pass
    def f7(self,seq):
        seen = set()
        seen_add = seen.add
        return [x for x in seq if not (x in seen or seen_add(x))]
    def crawl(self,platform,keyword):
        from selenium import webdriver
        from pyvirtualdisplay import Display
        import requests
        from bs4 import BeautifulSoup
        display = Display(visible=0, size=(800, 600))
        if(platform == "flipcart"):
            top_five_url_flipcart = []
            top_five_name_flipcart = []
            try:
                display.start()
                driver = webdriver.Chrome()
                url="https://www.flipkart.com/search?q=%s"%keyword
                driver.get(url)
                elements = driver.find_element_by_xpath("html/body/div[1]/div/div[2]/div[2]/div/div[2]")
                flp = elements.get_attribute('outerHTML')
                soup = BeautifulSoup(flp, "lxml")
                div_with_no_class  = soup.find_all("div", class_=False, id=False)
                ind = 0
                key = 0
                for i in div_with_no_class:
                    if(len(i.find_all('a')) > 0):
                        key = ind
                        break
                    ind+=1
                all_a_tag = div_with_no_class[key].find_all("a")
                all_url = []
                for i in all_a_tag:
                    tmp_url = "www.flipcart.com" + i['href']
                    all_url.append(tmp_url)
                top_five_url_flipcart = Crawler.f7(all_url)
                
                for u in top_five_url_flipcart:
                    tmp_name = u.split('/')[1]
                    top_five_name_flipcart.append(tmp_name)
            except Exception as e:
                print(e)
            finally:
                driver.quit()
                display.stop()
                return top_five_url_flipcart[:5],top_five_name_flipcart[:5]
        elif(platform == 'amazon'):
            top_five_url_amazon = []
            top_five_name_amazon = []
            try:
                url = "http://www.amazon.in/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=" + keyword
                r = requests.get(url)
                data = r.content.decode(encoding='UTF-8')
                soup = BeautifulSoup(data, "lxml")
                tmp1 = soup.find_all('div',{"id":"atfResults"})
                tmp2 = tmp1[0].find_all('li',{"class":"s-result-item celwidget"})
                for li in tmp2:
                    u = li.find('a')['href']
                    #print u
                    top_five_url_amazon.append(u)
                    v = u.replace('http://www.amazon.in/','')
                    v = v.split('/')[0]
                    if v != '':
                        top_five_name_amazon.append(v)
                    #print v
            except Exception as e:
                print(e)
            finally:
                return top_five_url_amazon[:5],top_five_name_amazon[:5]

        elif(platform == 'snapdeal'):
            top_five_url_snapdeal = []
            top_five_name_snapdeal = []
            try:
                url = 'https://www.snapdeal.com/search?keyword='+ keyword
                r = requests.get(url)
                data = r.content.decode(encoding='UTF-8')
                soup = BeautifulSoup(data,'lxml')
                all_link = soup.find_all("div",{'class':'product-desc-rating '})
                for i in all_link:
                    link = i.find('a')
                    name = i.find('p')
                    top_five_name_snapdeal.append(name.get_text())
                    top_five_url_snapdeal.append(link['href'])
            except Exception as e:
                print(e)
            finally:
                return top_five_url_snapdeal[:5],top_five_name_snapdeal[:5]

        else:
            print("platform name does not match with either amazon or flipcart\n")

        def __str__(self):
            return str(self.name)
# if __name__ == '__main__':
# 	a,b = _crawl('flipcart','moto g3')
# 	print a
# 	print b
