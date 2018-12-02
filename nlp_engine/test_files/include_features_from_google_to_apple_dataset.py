## Features like number of installs, age group, etc
## The code works but finding similar app name between the 2 dataset and including new column values for each app name will take around 10 hours
## Another solution is - finding similar app name in the google dataset sparse array, everytime a new decription is entered in real time



from sklearn.feature_extraction.text import TfidfVectorizer ## TFIDF calculation
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text

import nltk
from nltk.stem.wordnet import WordNetLemmatizer ## pos tagging and lemmatization
from nltk.corpus import wordnet
lemmatizer = WordNetLemmatizer()
from nltk.tokenize import RegexpTokenizer ## Tokenizer which removes punctuation

import pandas as pd ## Read and manipulate csv

from langdetect import detect ## Detect Language

import pickle ## pickle the model

# import numpy
# numpy.set_printoptions(threshold=numpy.nan) ## To print the full NumPy array when jupyter notebook truncates the stdout with ... in between

## Reading from csv using pandas
path = 'C:\\Users\\shrke\\Desktop\\272 Project\\Google store dataset\\'
data_full = pd.read_csv(path + "googleplaystore.csv")



description_array = []
## Array that stores all descriptions

        

## Append all descriptions into a single array
for i in range(len(data_full)):  
    description_array.append(data_full.iloc[i]['App'])

description_array[0]

vectorizer = TfidfVectorizer(stop_words = 'english')   

## tokenize and build vocabulary
vectorizer.fit(description_array)
print (len(vectorizer.vocabulary_))

all_documents_encoded = []
for i in range(len(description_array)):
    vector = vectorizer.transform([description_array[i]]) ## make sparse array
    ## summarize encoded vector
    vector_array = vector.toarray()
    all_documents_encoded.append(vector_array[0]) 
    
all_documents_encoded[1] 
print (len(all_documents_encoded))

path1 = 'C:\\Users\\shrke\\Desktop\\272 Project\\Apple store dataset\\'
data_full1 = pd.read_csv(path1 + "AppleStore.csv")
data_full1['installs'] = 0
data_full1.to_csv(path1 + "AppleStore.csv")

data_full1.loc[1,'Installs']= data_full.iloc[3913]['Installs']
data_full1.to_csv(path1 + "AppleStore.csv")

def sortTopXpercent(all_documents_similarity, topXpercent):

    x = 1
    while(x<=topXpercent):

        for i in range(len(all_documents_similarity)-1, -1, -1):
            
            if(i == 0):
                continue
            if(all_documents_similarity[i]>all_documents_similarity[i-1]):
                temp = all_documents_similarity[i]
                all_documents_similarity[i] = all_documents_similarity[i-1]
                all_documents_similarity[i-1] = temp
                
        x = x+1

    all_documents_similarity_sorted_topXpercent = all_documents_similarity[:topXpercent]

    return all_documents_similarity_sorted_topXpercent

for i in range(0, 7197):
    test_description_modified = data_full1.iloc[i]['track_name']
    print (test_description_modified)
    test_document_vector = vectorizer.transform([test_description_modified])
    test_document_encoded = (test_document_vector.toarray()) 
    #print (test_description_modified)
    
    
    ## Cosine Similarity:
    all_documents_similarity = []
    ## all_documents_similarity is a array in which we save the similarity and the primary key/index together as we will have to sort the list for selecting top similar descriptions, so we need to save the indexes as well
    for i in range(len(all_documents_encoded)):
        all_documents_similarity.append([cosine_similarity([all_documents_encoded[i]],test_document_encoded), i])

    ## Sort all similarities in desc order    
    all_documents_similarity_sorted = sortTopXpercent(all_documents_similarity, 1) 
    print (all_documents_similarity_sorted[0][1])
    print (data_full.iloc[all_documents_similarity_sorted[0][1]]['Installs'])
    print (data_full1.loc[(i-1),'Installs'])
    data_full1.loc[(i-1),'Installs']= data_full.iloc[all_documents_similarity_sorted[0][1]]['Installs']
    data_full1.to_csv(path1 + "AppleStore.csv")
    
