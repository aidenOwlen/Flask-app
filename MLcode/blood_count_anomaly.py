# -*- coding: utf-8 -*-

import pickle
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.metrics import confusion_matrix
import sqlite3


	
def prepare_data():
	"""
	We gonna stack all blood count dataset files using pds, drop unnecessary columns and fill null columns
	Data normalization / Standarization doesn't seem reasonable to me in this step, because we're aiming to 
	detect outliers.
	Return prepared DataFrame
	"""
	blood_count_files = ["LAB25.XPT","CBC_H.XPT","CBC_D.XPT","L25_C.XPT","L25_B.XPT"]
	blood_count_files_path = ["dataset/{}".format(x) for x in blood_count_files]
	df = pd.concat([pd.read_sas(x) for x in blood_count_files_path],axis=0)
	df = df.rename(columns={"LBXWBCSI":"Globules blancs","LBDLYMNO":"Lymphocytes",
		"LBDMONO":"Monocytes", "LBDNENO":"Neutrophiles", "LBDEONO":"Eosinophiles",
		"LBDBANO":"Basophiles","LBXRBCSI":"RedCellCount","LBXHGB":"Hemoglobine",
		"LBXHCT":"Hematocrite %", "LBXMCVSI":"VGM", "LBXMCHSI":"TCMH","LBXMC":"CCMH",
		"LBXRDW":"Red Cell Distribution Width %", "LBXPLTSI":"Plaquette",
		"LBXMPSI":"Volume Plaquettaire Moyen"})
	#First columns is just patient reference and other columns are values of white cells in percent, 
	#we already have that in real number, so let's remove them.
	columns_to_drop = ["SEQN", "LBXLYPCT","LBXMOPCT","LBXNEPCT", "LBXEOPCT", "LBXBAPCT"].
	df.drop(columns_to_drop,axis=1, inplace = True) 

	#Filling all empty columns with the feature mean.
	#I don't think it makes sense to fill them using linear regression
	for column in df.columns:
		df[column].fillna(df[column].mean(), inplace=True)
	return pd.DataFrame(data=df)

def push_blood_dataframe_to_sqlite2(data):
	"""
	Push prepared data to sqlite3 blood_counts.db, as a BLOODCOUNT table
	"""
	conn = sqlite3.connect("blood_counts.db")
	df.to_sql(name="BLOODCOUNT",con=conn)
	conn.close()
	

def isolation_forest(data):

	#Let's run an isolationForest algorithm, to detect outliers ( 0.1 )
	contamination = 0.1
	model = IsolationForest(contamination = contamination, n_estimators = 1000)
	model.fit(df)
	#df["iforest"] = pd.Series(model.predict(df))
	##c = [x for x in df["iforest"] if x == -1]
	#print(len(c))
	#print(df.shape)
	return model
	



if __name__ == "__main__":
	df = prepare_data()  #prepare data
	print(df.mean()) # Print the mean column-wise

	model = isolation_forest(df) # Run isolation forest to detect outliers ( 0.1)
	pickle.dump(model, open("model.pkl","wb")) #Save model
	df["iforest"] = pd.Series(model.predict(df)) # Get prediction, outlier = -1 else = 1
	c = [x for x in df["iforest"] if x == -1] #list of outliers
	print(len(c)) #Nuber of outliers
	print(df[df["iforest"] == -1])