import re
import numpy as np
import pandas as pd
from connection import engine
class Labeling():
	def __init__(self):
		pass
	def __extract_table__(self,tbname=None):
		conn = engine.raw_connection()
		print 'test1',tbname
		df = pd.read_sql('select * from %s'%tbname, con=conn)  
		conn.close()
		return df

	def __filtering__(self,df=None):
		ind_with_keywords = df.review.str.\
		contains('warranty|amazon|snapdel|delivery|shipping|service|transporting|packing|package',\
		flags=re.IGNORECASE, regex=True, na=False)
		return df[ind_with_keywords]

	def __labeling__(self,df=None):
		df['label'] = np.nan
		# df['label'] = pd.Series(np.zeros(len(df)))
		df.loc[df.rating>3,'label'] = 1
		df.loc[df.rating<=3,'label'] = 0
		return df

	def __process_train_data__(self,tbname1,tbname2):
		df_ama = self.__extract_table__(tbname1)
		df_snap = self.__extract_table__(tbname2)
		df_ama_filtered = self.__filtering__(df_ama)
		df_snap_filtered = self.__filtering__(df_snap)
		df_ama_labeled = self.__labeling__(df_ama_filtered)
		df_snap_labeled = self.__labeling__(df_snap_filtered)
		df_labeled = pd.concat([df_ama_labeled[['review','label']], df_snap_labeled[['review','label']]])
		return df_labeled

	def __process_test_data__(self,tbname):
		df = self.__extract_table__(tbname)
		df_filtered = self.__filtering__(df)
		return df_filtered[['review']]



