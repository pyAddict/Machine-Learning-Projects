from django.http import HttpResponse

from django.template import loader
from django.template.loader import get_template
# def index(request):
#     latest_question_list = ['a','b','c']
#     template = loader.get_template('product/index.html')
#     context = {
#         'latest_question_list': 'string',
#     }
#     return HttpResponse(template.render(context, request))


from django.shortcuts import render
from django.http import HttpResponseRedirect

from product.forms import NameForm
from product.forms import SelectForm

from product.crawlers import Crawler
import amazon_crawl
from amazon_crawl.main_scrapy_amazon import main_scrapy
from snapdeal_crawl.main_snapdeal import main_snap
from review_analysis.main_sentiments import main_sent
global a #amazon_url
global b #amazon_name
global c #snapdeal_url
global d #snapdeal_name
global resultt
def name(request):
    # if this is a POST request we need to process the form data
    obj = Crawler()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        # print(request.POST)
        form = NameForm(request.POST)
        print("debug 0")
        result = str(form["your_product"].value())

        print(form["your_product"].value())
        # check whether it's valid:
        if form.is_valid():
            print("insidwee......")
            print("debbuugg")
            print(form["your_product"].value().decode('UTF-8'))
            a,b = obj.crawl('amazon',form["your_product"].value().decode('UTF-8'))

            dictionary = dict(zip(b, a))
            print(dictionary)
            c,d = obj.crawl('snapdeal',form["your_product"].value().decode('UTF-8'))
            print(c)
            print(d)
            dictionary2 = dict(zip(d, c))
            print(dictionary2)
            return render(request, "name.html" , {'form' : form ,'amazon_url_list':a,'amazon_names':dictionary , 'flipkart_url_list':c,'flipkart_names':dictionary2})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})

def results(request):  
    # text = request.session.get("text", None)
    amazon_result_pos = 5
    amazon_result_neg = 5
    snapdeal_result_pos= 6
    snapdeal_result_neg = 4
    

    c = {'amazon_result_pos':amazon_result_pos,'amazon_result_neg':amazon_result_neg,'snapdeal_result_pos':snapdeal_result_pos,'snapdeal_result_neg':snapdeal_result_neg }
    return render(request, 'results.html', c)




def index(request):
    latest_question_list = ['a','b','c']
    template = get_template('/home/harshita/Desktop/myproduct/product/templates/product/index.html')
    context = {
        'latest_question_list': 'string',
    }
    return HttpResponse(template.render(context, request))

def input_crawl(result):
    a,b = Crawler_crawl('amazon','moto g3')
    print(a)
    print(b)

def selected(request):
    # if this is a POST request we need to process the form data
    global resultt
    if request.method == 'POST':
        form = SelectForm(request.POST)
        print("debugggg 0")
        resultt = (form["selected_choice"].value())
        #print(resultt)
        print(form["selected_choice"].value())
        # check whether it's valid:
        if form.is_valid():
            print("debug_inside")
        else:
            print("debug !form is_valid")

        # main_scrapy()
        # main_snap()
        main_sent()
        import review_analysis
        from review_analysis import training

        
        pos_rev_amz = training.pos_review[0]
        neg_rev_amz = training.neg_review[0]
        tot_rev_amz = training.tot_review[0]
        pos_rev_snap = training.pos_review[1]
        neg_rev_snap = training.neg_review[1]
        tot_rev_snap = training.tot_review[1]
        return render(request, "selected.html" , {'form' : form,'resultt':resultt,'pos_rev_amz' : pos_rev_amz,'neg_rev_amz':neg_rev_amz,'tot_rev_amz':tot_rev_amz,'pos_rev_snap' : pos_rev_snap,'neg_rev_snap':neg_rev_snap,'tot_rev_snap':tot_rev_snap})

    