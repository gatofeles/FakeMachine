import numpy as np
import pandas as pd
import spacy
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

nlp = spacy.load('pt_core_news_lg')
b5PostDf = pd.read_csv('b5corpus/post-utf8-singleFile.csv', on_bad_lines='skip', sep=';')
types = ['ext', 'agr', 'con', 'neu', 'ope']
perLabelsData = {}
perPredictors = {}

# print(b5PostDf.head())
# print("null values = "+str(b5PostDf.isnull().sum()))
# for per in types:
#     print(per+ "Count = " +str(b5PostDf[per].value_counts()))


lowerString = [entry.lower() for entry in b5PostDf['string']]
lemmaString = {'string':[]}

for sentence in lowerString:
  doc = nlp(sentence)
  newSentence = ''
  for word in doc:
    if word.text not in nlp.Defaults.stop_words:
      newSentence += " "+word.lemma_
  lemmaString['string'].append(newSentence)

X = lemmaString['string']

for per in types:
    perLabelsData[per] = b5PostDf[per]
    
for per in types:
    #building pipeline
    print("for "+per)
    X_train, X_test , y_train, y_test =  train_test_split(X, perLabelsData[per], test_size=0.3, random_state=10)
    perPredictors[per] = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LinearSVC())])
    perPredictors[per].fit(X_train, y_train)
    
    predict = perPredictors[per].predict(X_test)
    
    print(confusion_matrix(y_test, predict))
    print(classification_report(y_test, predict))
    
    
print("Raul pred " + str(perPredictors['agr'].predict(["Eu sou a luz das estrelas."])))