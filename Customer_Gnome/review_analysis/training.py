import pandas as pd
import nltk
import numpy as np
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re
from sklearn.feature_extraction.text import CountVectorizer
global pos_review
global neg_review
global tot_review
pos_review = []
neg_review = []
tot_review = []
class Train_and_Predict():
	def __init__(self):
		pass
	def __review_to_words__(self,raw_review):
	    # Function to convert a raw review to a string of words
	    # The input is a single string (a raw movie review), and 
	    # the output is a single string (a preprocessed movie review)
	    #
	    # 1. Remove HTML
	    review_text = BeautifulSoup(raw_review,'lxml').get_text() 
	    #
	    # 2. Remove non-letters        
	    letters_only = re.sub("[^a-zA-Z]", " ", review_text) 
	    #
	    # 3. Convert to lower case, split into individual words
	    words = letters_only.lower().split()                             
	    #
	    # 4. In Python, searching a set is much faster than searching
	    #   a list, so convert the stop words to a set
	    stops = set(stopwords.words("english"))                  
	    # 
	    # 5. Remove stop words
	    meaningful_words = [w for w in words if not w in stops]   
	    #
	    # 6. Join the words back into one string separated by space, 
	    # and return the result.
	    return( " ".join( meaningful_words )) 


	def __data_preprocessing__(self,df1=None,df2=None):
		self.df_train = df1
		self.df_test = df2
		num_reviews_train = self.df_train["review"].size
		num_reviews_test = self.df_test["review"].size
		rev1 = self.df_train.review.values
		rev2 = self.df_test.review.values
		print "Cleaning and parsing the training set reviews...\n"
		clean_train_reviews = []
		clean_test_reviews = []
		for i in xrange( 0, num_reviews_train ):
		# If the index is evenly divisible by 100, print a message
			if( (i+1)%100 == 0 ):
				print "Review %d of %d\n" % ( i+1, num_reviews_train )                                                                    
			clean_train_reviews.append( self.__review_to_words__( rev1[i] ))

		for i in xrange( 0, num_reviews_test ):
		# If the index is evenly divisible by 100, print a message
			if( (i+1)%100 == 0 ):
				print "Review %d of %d\n" % ( i+1, num_reviews_test )                                                                    
			clean_test_reviews.append( self.__review_to_words__( rev2[i] ))

		print "Creating the bag of words...\n"
		# Initialize the "CountVectorizer" object, which is scikit-learn's
		# bag of words tool.  
		vectorizer = CountVectorizer(analyzer = "word",   \
		                             tokenizer = None,    \
		                             preprocessor = None, \
		                             stop_words = None,   \
		                             max_features = 5000) 

		# fit_transform() does two functions: First, it fits the model
		# and learns the vocabulary; second, it transforms our training data
		# into feature vectors. The input to fit_transform should be a list of 
		# strings.
		train_data_features = vectorizer.fit_transform(clean_train_reviews)

		# Numpy arrays are easy to work with, so convert the result to an 
		# array
		train_data_features = train_data_features.toarray()
		test_data_features = vectorizer.transform(clean_test_reviews)
		test_data_features = test_data_features.toarray()

		return train_data_features,test_data_features


	def __modeling__(self,train_data_features=None,test_data_features=None):
		global pos_review
		global neg_review
		global tot_review
		self.train_data_features = train_data_features
		self.test_data_features = test_data_features
		from sklearn.cross_validation import KFold
		from sklearn.metrics import accuracy_score
		import numpy as np
		from sklearn.ensemble import RandomForestClassifier
		forest = RandomForestClassifier(n_estimators = 100) 
		n_folds = 10
		acc = []
		x = self.train_data_features
		y = np.array(self.df_train['label'])
		n = len(x)
		cnt = 1
		kf = KFold(n,n_folds,shuffle=False,random_state=None)
		print self.train_data_features.shape,self.test_data_features.shape
		print "Training the random forest..."
		for train_index,test_index in kf:
			print 'training part-%d'%cnt
			x_train,x_test = x[train_index],x[test_index]
			y_train,y_test = y[train_index],y[test_index]
			forest.fit(x_train,y_train)
			y_pred = forest.predict(x_test)
			acc.append(accuracy_score(y_test,y_pred))
			print 'accuracy score-%f'%accuracy_score(y_test,y_pred)
			cnt+=1

		print "over-all accuracy on training data using 10 fold cross-validation = %f" %(np.mean(np.array(acc)))
		print np.mean(np.array(acc))
		# Use the random forest to make sentiment label predictions
		result = forest.predict(self.test_data_features)
		ones = 0
		zeros = 0
		for i in result:
			if i == 0:
				zeros += 1
			elif i == 1:
				ones += 1

		print 'total number of reviews.............. :%d'%self.df_test['review'].size
		print 'total positive review predicted : %d'%ones
		print 'total negative review predicted : %d'%zeros

		pos_review.append(ones)
		neg_review.append(zeros)
		tot_review.append(self.df_test['review'].size)
		print ("debug....positive_reviews.....")
		print pos_review
