import nltk,itertools,string,os,csv
from nltk.stem import PorterStemmer
ps = PorterStemmer()
import pandas as pd
import numpy as np
import ast

def clean_competency_text(text):
    #text = unicode(text, errors='replace')
    punct = set(string.punctuation)
    punct.remove('+')
    stop_words = set(nltk.corpus.stopwords.words('english'))
    try:
        candidates = ast.literal_eval(text)
        #candidates = candidates.replace(" ","")
    except Exception as e:
        print "exception type-1...",e
        try:
            candidates = [word.lower() for word in nltk.word_tokenize(text) if word.lower() not in stop_words \
                          and not all(char in punct for char in word)]
            
        except Exception as e:
            print "exception-type-2...",e
            text = unicode(text, errors='replace')
            candidates = [word.lower() for word in nltk.word_tokenize(text) if word.lower() not in stop_words \
                          and not all(char in punct for char in word)]
    finally:
        if len(candidates) > 0 :
            #print candidates
            candidates = ','.join(w for w in candidates if w is not None)
        else:
            candidates = "None"
        return candidates

def extract_candidate_words(text, good_tags=set(['JJ','JJR','JJS','NN','NNP','NNS','NNPS'])):
    text = unicode(text, errors='replace')
    # exclude candidates that are stop words or entirely punctuation
    punct = set(string.punctuation)
    punct.remove('+')
    stop_words = set(nltk.corpus.stopwords.words('english'))
    # tokenize and POS-tag words
    tagged_words = itertools.chain.from_iterable(nltk.pos_tag_sents(nltk.word_tokenize(sent)
                                                                    for sent in nltk.sent_tokenize(text)))
    # filter on certain POS tags and lowercase all words
    candidates = [word.lower() for word, tag in tagged_words
                  if tag in good_tags and word.lower() not in stop_words
                  and not all(char in punct for char in word)]

    return candidates

def preprocessing(filename):
    print 'pre processing '+filename+'started ....'
    file_obj = csv.reader(open('.'+os.path.sep+'data'+os.path.sep+filename, 'rb'))
    pre_processed_file = csv.writer(open('.'+os.path.sep+'data'+os.path.sep+'pre_process_'+filename, "wb"),\
                                    quoting=csv.QUOTE_NONNUMERIC)
    
    if filename == 'Train_data_1.csv':
        for row in file_obj:
            title_text = row[3]
            jd_text = row[4]
            comp_text = row[5]
            tmp_title_text = extract_candidate_words(title_text)
            pre_proc_title_text = ' '.join(w.encode('utf-8') for w in tmp_title_text)
            tmp_jd_text = extract_candidate_words(jd_text)
            pre_proc_jd_text = ' '.join(w.encode('utf-8') for w in tmp_jd_text)
            pre_proc_comp_text = clean_competency_text(comp_text)
            if not pre_proc_comp_text:
                print comp_text
            pre_processed_file.writerow([row[0],pre_proc_title_text,pre_proc_jd_text,pre_proc_comp_text])
            
    elif filename == 'Test_data.csv':
        for row in file_obj:
            title_text = row[3]
            jd_text = row[4]
            #pre_proc_title_text = filter_stop_words_and_punct(title_text)
            pre_proc_title_text = title_text
            tmp_jd_text = extract_candidate_words(jd_text)
            pre_proc_jd_text = ' '.join(w.encode('utf-8')for w in tmp_jd_text)
            pre_processed_file.writerow([row[0],pre_proc_title_text,pre_proc_jd_text])
    print "preprocessing done ...."
        
def missing_value_imputation(filename,ind_with_jd_nan,dic):
	print 'missing_value imputation is going on ......'
	data = pd.read_csv('./data/%s'%filename)
	cnt = 500 
	for ind_1 in ind_with_jd_nan:
	    cnt += 1
	    if float(cnt)%500 == 0:
	        print "500 more rows completed...."
	    tmp_title = data.title[ind_1]
	    #print tmp_title
	    if tmp_title in dic.keys():
	        #print type(dic[tmp_title][0])
	        txt = ' '.join(str(w) for w in dic[tmp_title])
	    else:
	        txt = tmp_title
	    data.jd_txt[ind_1] = txt
	print 'missing_value imputation done !!'
	data.to_csv('./data/imputed_pre_processed-data.csv',index=False)

#create dictioanry of keys as title and items as jd_txt
#To reduce computation
def _create_dic_of_title(train_modified):
    dic = {}
    for row in xrange(train_modified.shape[0]):
        key = train_modified.title[row]
        if key in dic.keys():
            tmp = dic[key]
            if not pd.isnull(train_modified.jd_txt[row]):
                tmp.append(train_modified.jd_txt[row])
            else:
                tmp.append(train_modified.title[row])
            dic[key] = tmp
        else:
            tmp = []
            if not pd.isnull(train_modified.jd_txt[row]):
                tmp.append(train_modified.jd_txt[row])
            else:
                tmp.append(train_modified.title[row])
            dic[key] = tmp
    return dic

def main():
    train = pd.read_csv('./data/Train_data.csv')

    #Find index where competency is not null in train
    ind_with_compe = np.where(train.competencies_text.notnull())[0]
    train = train.loc[ind_with_compe]

    train.to_csv('./data/Train_data_1.csv',index=False)
    del(train)
    preprocessing("Train_data_1.csv")
    preprocessing("Test_data.csv")

    train_modified = pd.read_csv('./data/pre_process_Train_data_1.csv')
    test_modified = pd.read_csv('./data/pre_process_Test_data.csv')
    print train_modified.apply(lambda x: sum(x.isnull()))
    print test_modified.apply(lambda x: sum(x.isnull()))
    #We have to fill missing value of jd_txt only
    ind_with_jd_nan = np.where(train_modified.jd_txt.isnull())[0]
    dic = _create_dic_of_title(train_modified)
    print len(dic.keys())
    missing_value_imputation('pre_process_Train_data_1.csv',ind_with_jd_nan,dic)


if __name__ == '__main__':
    main()