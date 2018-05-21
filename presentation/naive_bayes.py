from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
import pandas as pd
from time import time
import nltk
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
import sklearn.metrics
from pandas import DataFrame,Series
import matplotlib.pyplot as plt

training_time_container={'b_naive_bayes':0,'mn_naive_bayes':0,'random_forest':0,'linear_svm':0}
prediction_time_container={'b_naive_bayes':0,'mn_naive_bayes':0,'random_forest':0,'linear_svm':0}
accuracy_container={'b_naive_bayes':0,'mn_naive_bayes':0,'random_forest':0,'linear_svm':0}

dataframe = document_token_new.copy()
dataframe['class'] = dataframe['c_id']
dataframe = dataframe[dataframe['class'] != 11]
dataframe.__delitem__('c_id')
dataframe.__delitem__('doc_id')
dataframe.__delitem__('token_id')

corpus=dataframe.token_text
vectorizer = TfidfVectorizer()
tfidf_matrix=vectorizer.fit_transform(corpus).todense()

variables = tfidf_matrix
labels = dataframe.iloc[:,12].values
labels = labels.astype('float64')

dataframe_notext = dataframe.iloc[:,1:]
tfidf_matrix = pd.DataFrame(tfidf_matrix)

for column in list(dataframe_notext.columns.values):
    tfidf_matrix[str(column)] = 0.0

counter = 0
for index, row in dataframe_notext.iterrows():
    for column in list(dataframe_notext.columns.values):
        tfidf_matrix.at[counter,column] = row[str(column)]
        
    counter+=1


'''
variables_train, variables_test, labels_train, labels_test=train_test_split(
        variables, labels, test_size=.3)

print('Shape of Training Data: '+str(variables_train.shape))
print('Shape of Test Data: '+str(variables_test.shape))
'''
################################################
variables = tfidf_matrix.iloc[:,:].values
labels = dataframe.iloc[:,12].values
labels = labels.astype('float64')


################################################
from sklearn.naive_bayes import BernoulliNB
bnb_classifier=BernoulliNB()
t0=time()
bnb_classifier=bnb_classifier.fit(variables,labels)
training_time_container['b_naive_bayes']=time()-t0

t0=time()
bnb_predictions=bnb_classifier.predict(variables)
prediction_time_container['b_naive_bayes']=time()-t0
prediction_time_container['b_naive_bayes']

nb_ascore=sklearn.metrics.accuracy_score(labels, bnb_predictions)
accuracy_container['b_naive_bayes']=nb_ascore

print("Bernoulli Naive Bayes Accuracy Score: %f"%accuracy_container['b_naive_bayes'])
print("Training Time: %f"%training_time_container['b_naive_bayes'])
print("Prediction Time: %f"%prediction_time_container['b_naive_bayes'])