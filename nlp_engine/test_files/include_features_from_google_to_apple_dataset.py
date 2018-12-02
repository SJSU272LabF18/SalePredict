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
