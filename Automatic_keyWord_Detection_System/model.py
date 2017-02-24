import nltk,itertools,string,os,csv,sys
csv.field_size_limit(sys.maxsize)
from nltk.stem import PorterStemmer
ps = PorterStemmer()
import pandas as pd
import numpy as np
import pickle
from itertools import product
import pymongo
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
client = MongoClient()
db = client.edge_task

title_threshold = 0.7
body_threshold = 0.9
support_threshold = 1


def _find_bigrams(text):
    from nltk.collocations import BigramCollocationFinder
    from nltk.metrics import BigramAssocMeasures
    token = nltk.word_tokenize(text)
    bigram_finder = BigramCollocationFinder.from_words(token)
    bigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 500)
    bigram_list = [''.join(w) for w in bigrams]
    bigram_string = ','.join(bigram_list)
    return bigram_string

def _find_most_frequent_words(text):
	all_words = [w.lower() for w in text.split(',')]
	fdist = nltk.FreqDist(all_words)
	fdist = fdist.most_common()
	return fdist[0][0]

def find_all_combinations_helper(train_filename,index):
	cnt = 100
	cnttt = 0
	print 'find all combination running.....'
	with open(r'.'+os.path.sep+'data'+os.path.sep+train_filename) as r, \
	open(r'.'+os.path.sep+'data'+os.path.sep+str(index)+'_unigram.tmp', "w") as w,\
	open(r'.'+os.path.sep+'data'+os.path.sep+str(index)+'_bigram.tmp', "w") as ww:
	    header = r.next()
	    rdr = csv.reader(r)
	    for row in rdr:
	        a=row[index].lower()#title ans jd_txt acc to index value
	        b=row[3].lower()
	        try:
	            c = _find_bigrams(a)
	        except Exception as ZeroDivisionError:
	            print "ZeroDivisionError"
	            a = sorted(set(a.split()))
	            a = ' '.join(a)
	            c = _find_bigrams(a)
	        for x, y in product(a.split(), b.split(',')):
	            if x and y:
	                w.write("{},{}\n".format(x, y))
	        for xx, yy in product(c.split(','), b.split(',')):
	            if xx and yy:
	                ww.write("{},{}\n".format(xx, yy))

	word_tag_combination_counter = {}
	with open('.'+os.path.sep+'data'+os.path.sep+str(index)+'_unigram.tmp','rb') as file_name_1,\
	open('.'+os.path.sep+'data'+os.path.sep+str(index)+'_bigram.tmp','rb') as file_name_2:
	    reader1=csv.reader(file_name_1)
	    for row in reader1:
	        pair=row[0]+'_'+row[1]
	        if pair in word_tag_combination_counter:
	            word_tag_combination_counter[pair]+=1
	        else:
	            word_tag_combination_counter[pair]=1
	            
	    reader2=csv.reader(file_name_2)
	    for row in reader2:
	        pair=row[0]+'_'+row[1]
	        if pair in word_tag_combination_counter:
	            word_tag_combination_counter[pair]+=1
	        else:
	            word_tag_combination_counter[pair]=1
	            
	print 'word-tag-counter-length %d'%len(word_tag_combination_counter)
	word_counter = {}
	with open('.'+os.path.sep+'data'+os.path.sep+train_filename,'rb') as file_name:
	    reader=csv.reader(file_name)
	    for row in reader:
	    	a = row[index].lower()
	    	try:
	            c = _find_bigrams(a)
	        except Exception as ZeroDivisionError:
	            print "ZeroDivisionError"
	            a = sorted(set(a.split()))
	            a = ' '.join(a)
	            c = _find_bigrams(a)
	        for word in row[index].lower().split():
	            if word in word_counter:
	                word_counter[word]+=1
	            else:
	                word_counter[word]=1
	                
	        for bigra_word in c.split(','):
	            if bigra_word in word_counter:
	                word_counter[bigra_word]+=1
	            else:
	                word_counter[bigra_word]=1
	print 'word-counter-length %d'%len(word_counter)
	#Lets save word_counter and word_tag_counter as pickle file
	# with open('./data/word_count.pickle', 'wb') as file_n:
	# 	pickle.dump(word_counter, file_n)
	# with open('./data/word_tag_count.pickle', 'wb') as file_n:
	# 	pickle.dump(word_tag_combination_counter, file_n)
	if(index == 1):
	    probabilities = db['title_prob']
	else:
	    probabilities = db['jd_prob']
	    
	for pair in word_tag_combination_counter:
	    try:
	        word = pair.split('_')[0]
	        #word.encode('utf-8')
	        #word = unicode(word, errors = 'ignore')
	        tag = pair.split('_')[1]
	        #tag = unicode(tag, errors = 'ignore')
	        #tag.encode('utf-8')
	        support = word_tag_combination_counter[pair]
	        #support.encode('utf-8')
	        #support = unicode(support, errors = 'replace')
	        if word in word_counter:
	            score = float(word_tag_combination_counter[pair]) / float(word_counter[word])
	        else:
	        	cnttt+=1
	        	score = 0 
	        if index==1:
	            if score>=title_threshold and support>=support_threshold:
	                probability = {'word':word,'tag':tag, 'score':score}
	                probabilities.insert(probability)
	        else:
	            if score>=body_threshold and support>=support_threshold:
	                probability = {'word':word,'tag':tag, 'score':score}
	                probabilities.insert(probability)
	    except Exception as e:
	    	print e
	        # cnt += 1
	        # if float(cnt)%100 == 0:
	        #     print "100 more  exception handled---",e
	        # pass
	#             try:
	#                 tag = pair.split()[1]
	#                 probability = {'word':word,'tag':tag, 'score':0}
	#                 probabilities.insert(probability)
	#             except Exception as e:
	#                 print e
	#                 probability = {'word':word,'tag':"None", 'score':0}
	#                 probabilities.insert(probability)     
	            
	print 'done...all combination are successfully formed !!'
	print 'total word not found %d'%cnttt


def F1_score(tags,predicted):
    tags = set(tags)
    predicted = set(predicted)
    tp = len(tags & predicted)
    fp = len(predicted) - tp
    fn = len(tags) - tp
 
    if tp>0:
        precision=float(tp)/(tp+fp)
        recall=float(tp)/(tp+fn)
 
        return 2*((precision*recall)/(precision+recall))
    else:
        return 0

def run_model(test_filename,t_t=0.5,b_t=0.4):
	title_threshold = t_t
	body_threshold = b_t
	output_filename = "predicted_tag_on_test_data.csv"
	titles_probabilities = db['title_prob']
	titles_probabilities.create_index([("word", ASCENDING)])
	body_probabilities = db['jd_prob']
	body_probabilities.create_index([("word", ASCENDING)])
	print 'predicting...'
	test_file_object = csv.reader(open('.'+os.path.sep+'data'+os.path.sep+test_filename, 'rb'))
	header = test_file_object.next()
	output_file = csv.writer(open('.'+os.path.sep+'data'+os.path.sep+output_filename, "wb"),quoting=csv.QUOTE_NONNUMERIC)
	output_file.writerow(['Id','Tags'])
	for row in test_file_object:
	    predicted_tags = []
	    # find tags based on title
	    for word in row[1].lower().split():
	        word = unicode(word, errors = 'replace')
	        find_result = titles_probabilities.find({'word':word})#,'score':{'$gte':title_threshold}})
	        for tag_result in find_result:
	            if not tag_result['tag'] in predicted_tags:
	                predicted_tags.append(tag_result['tag'])

	    a=row[1].lower()#title ans jd_txt acc to index value
	    try:
	        c1 = _find_bigrams(a)
	    except Exception as ZeroDivisionError:
	        print "ZeroDivisionError"
	        a = sorted(set(a.split()))
	        a = ' '.join(a)
	        c1 = _find_bigrams(a)
	    for word in c1.split(','):
	        word = unicode(word, errors = 'replace')
	        find_result = titles_probabilities.find({'word':word})
	        for tag_result in find_result:
	            if not tag_result['tag'] in predicted_tags:
	                predicted_tags.append(tag_result['tag'])
	    # find tags based on body
	    for word in row[2].lower().split():
	        word = unicode(word, errors = 'replace')
	        find_result = body_probabilities.find({'word':word})#,'score':{'$gte':body_threshold}})
	        for tag_result in find_result:
	            tx = tag_result['tag'] + ','
	            if tx not in predicted_tags:
	                predicted_tags.append(tx)
	    a=row[2].lower()#title ans jd_txt acc to index value
	    try:
	        c2 = _find_bigrams(a)
	    except Exception as ZeroDivisionError:
	        print "ZeroDivisionError"
	        a = sorted(set(a.split()))
	        a = ' '.join(a)
	        c2 = _find_bigrams(a)
	    for word in c2.split(','):
	        word = unicode(word, errors = 'replace')
	        find_result = body_probabilities.find({'word':word})
	        for tag_result in find_result:
	            if not tag_result['tag'] in predicted_tags:
	                predicted_tags.append(tag_result['tag'])
	    if not predicted_tags:
	    	predicted_tags.append(_find_most_frequent_words(c1))
	    	predicted_tags.append(_find_most_frequent_words(c2))
	    output_file.writerow([int(row[0]),' '.join(predicted_tags)])
	print 'prediction done....'

def test_model(train_filename):
	print 'testing model....'
	f1_output_filename = "f1_output_filename.csv"
	titles_probabilities = db['title_prob']
	titles_probabilities.create_index([("word", ASCENDING)])
	body_probabilities = db['jd_prob']
	body_probabilities.create_index([("word", ASCENDING)])
	#print 'testing...'
	test_file_object = csv.reader(open('.'+os.path.sep+'data'+os.path.sep+train_filename, 'rb'))
	header = test_file_object.next()
	output_file = csv.writer(open('..'+os.path.sep+'data'+os.path.sep+f1_output_filename, "wb"),quoting=csv.QUOTE_NONNUMERIC)
	output_file.writerow(['Id','F1 score'])
	max_to_test = 100
	f1_mean = 0
	i=0
	for row in test_file_object:
	    predicted_tags = []
	    # find tags based on title
	    for word in row[1].lower().split():
	        #word = unicode(word, errors = 'ignore')
	        find_result = titles_probabilities.find({'word':word,'score':{'$gte':title_threshold}})
	        for tag_result in find_result:
	            if not tag_result['tag'] in predicted_tags:
	                predicted_tags.append(tag_result['tag'])
	    a=row[1].lower()#title ans jd_txt acc to index value
	    try:
	        c1 = _find_bigrams(a)
	    except Exception as ZeroDivisionError:
	        print "ZeroDivisionError"
	        a = sorted(set(a.split()))
	        a = ' '.join(a)
	        c1 = _find_bigrams(a)
	    for word in c1.split(','):
	        #word = unicode(word, errors = 'ignore')
	        find_result = titles_probabilities.find({'word':word,'score':{'$gte':title_threshold}})
	        for tag_result in find_result:
	            if not tag_result['tag'] in predicted_tags:
	                predicted_tags.append(tag_result['tag'])
	    # find tags based on body
	    for word in row[2].lower().split():
	        #word = unicode(word, errors = 'ignore')
	        find_result = body_probabilities.find({'word':word,'score':{'$gte':body_threshold}})
	        for tag_result in find_result:
	            if tag_result['tag'] not in predicted_tags:
	                predicted_tags.append(tag_result['tag'])
	    a=row[2].lower()#title ans jd_txt acc to index value
	    try:
	        c2 = _find_bigrams(a)
	    except Exception as ZeroDivisionError:
	        print "ZeroDivisionError"
	        a = sorted(set(a.split()))
	        a = ' '.join(a)
	        c2 = _find_bigrams(a)
	    for word in c2.split(','):
	        #word = unicode(word, errors = 'ignore')
	        find_result = body_probabilities.find({'word':word,'score':{'$gte':body_threshold}})
	        for tag_result in find_result:
	            if not tag_result['tag'] in predicted_tags:
	                predicted_tags.append(tag_result['tag'])
	    true = row[3].lower().split(',')
	    if not predicted_tags:
	    	predicted_tags.append(_find_most_frequent_words(c1))
	    	predicted_tags.append(_find_most_frequent_words(c2))
	    pred = predicted_tags
	    true_len = len(true)
	    try:
	        pred = pred[:true_len]
	    except:
	        pred = pred
	    output_file.writerow([int(row[0]),F1_score(true,pred)])
	    f1_mean += F1_score(row[3].lower().split(','),predicted_tags)
	    i+=1
	    if i==max_to_test:
	        break
	#print 'done, F1 mean is '+str(float(f1_mean)/float(max_to_test))
	#print 'prediction....done !!'
	return float(f1_mean)/float(max_to_test)

def find_best_threshold(train_filename):
	global title_threshold
	global body_threshold
	maxi = 0
	t_t = 0
	b_t = 0
	cntt = 10
	for title_t in range(0, 10):
	    for body_t in range(0,10):
	    	cntt += 1
	    	if float(cntt)%10 == 0:
	    		print "10 more iteration completed in finding optimal thresholds......"
	        title_threshold = float(title_t)/float(10)
	        body_threshold = float(body_t)/float(10)
	        #print 'thresholds are ('+str(title_threshold)+','+str(body_threshold)+')'
	        acc = test_model(train_filename)
	        if(acc >= maxi):
	            maxi = acc
	            t_t = title_threshold
	            b_t = body_threshold
	print 'maximum f1 score %f'%maxi,'\n at threshold %f'%t_t,'\n and support %f'%b_t
	return t_t,b_t

def _combine_predicted_reslut(Test_file,Predicted_file):
	t = pd.read_csv('.' + os.path.sep + "data"+ os.path.sep + Test_file)
	p = pd.read_csv('.' + os.path.sep + "data"+ os.path.sep + Predicted_file)
	tags = p.Tags.tolist()
	t.competencies_text = tags
	t.to_csv('./data/predicted_final.csv',index=False)
	print 'final prediction done ... file saved as predicted_final.csv in data directory !!'

def main():
	find_all_combinations_helper("imputed_pre_processed-data.csv",1) #for title
	find_all_combinations_helper("imputed_pre_processed-data.csv",2) #for jd_txt 
	accuracy = test_model("imputed_pre_processed-data.csv")
	print 'F1 score got %f...'%accuracy
	t_t,b_t = find_best_threshold("imputed_pre_processed-data.csv")#Finding best threshold..
	run_model('pre_process_Test_data.csv',t_t,b_t)
	_combine_predicted_reslut("Test_data.csv","predicted_tag_on_test_data.csv")


if __name__ == '__main__':
	main()