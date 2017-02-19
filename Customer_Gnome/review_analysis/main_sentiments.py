def main_sent():
	import pandas as pd
	import define_variables
	from data_labeling import Labeling
	from training import Train_and_Predict
	train_tb1 = define_variables.table1
	train_tb2 = define_variables.table2
	test_tb1 = define_variables.table3
	test_tb2 = define_variables.table4

	obj = Labeling()
	df_train = obj.__process_train_data__(train_tb1,train_tb2)
	df_test_xiomi_ama = obj.__process_test_data__(test_tb1)
	df_test_xiomi_snap = obj.__process_test_data__(test_tb2)
	obj_model = Train_and_Predict()
	#df_test_xiomi_snap.to_csv('./xiomi_snapdeal.csv',index=False)
	df_train_preprocessed,df_test_preprocessed = obj_model.__data_preprocessing__(df_train,df_test_xiomi_ama)
	obj_model.__modeling__(df_train_preprocessed,df_test_preprocessed)
	print "Above result is of amazon"

	df_train_preprocessed,df_test_preprocessed = obj_model.__data_preprocessing__(df_train,df_test_xiomi_snap)
	obj_model.__modeling__(df_train_preprocessed,df_test_preprocessed)
	print "Above result is of snapdeal"







