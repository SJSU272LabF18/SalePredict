## to compare runtime with python inbuilt sorted function with lambda 
import time

from flask import Flask, request, jsonify

from sklearn.feature_extraction.text import TfidfVectorizer ## TFIDF calculation
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text

import nltk
from nltk.stem.wordnet import WordNetLemmatizer ## pos tagging and lemmatization
from nltk.corpus import wordnet
lemmatizer = WordNetLemmatizer()
from nltk.tokenize import RegexpTokenizer ## Tokenizer which removes punctuation

from langdetect import detect ## Detect Language
import pickle ## pickle the model
import scipy.sparse ## Convert sparse matrix to SciPy CSC matrix .npz




#import numpy as np

## TO BE DONE AS SOON AS SERVER STARTS RUNNING i.e description_array file should be kept open and running even when nobody is pinging on enter description
## Load full description array
description_array = pickle.load(open("description_array.pickle", "rb"))
## Keep max_features the same as that training the model
vectorizer = TfidfVectorizer(stop_words = 'english', max_features = 9500)   
## tokenize and build vocabulary
vectorizer.fit(description_array)
## Load all rating array
rating_array = pickle.load(open("rating_array.pickle", "rb"))
#print (rating_array[0])
## Load all track name array
track_name_array = pickle.load(open("track_name_array.pickle", "rb"))
#print (track_name_array[0])
## Load All Documents Encoded Sparse Array npz file
sparse_matrix = scipy.sparse.load_npz('sparse_matrix_actual.npz')
all_documents_encoded = sparse_matrix.todense()
# Sometimes sparse_matrix.todense() shows memory error. But trying after some time it doesnt show error



## Test Description - Pos tagging and lemmatization with nltk:
## POS Tagging and Lemmatization function      
## See 'pos_tagging_and_lemmatization' file full explanation       
regexp_tokenizer = RegexpTokenizer(r'\w+')        
def lemmatizeDescription(current_description):
    ## No need to include stop words restriction here ad TfidfVectorizer(stop_words = 'english') is added as vectorizer
    current_description.lower()
    tokenized_description = regexp_tokenizer.tokenize(current_description)
    tag = nltk.pos_tag(tokenized_description)
    lemmatized_list = []
    for i in range(len(tag)):
        lemmatized_list.append(lemmatizer.lemmatize(tag[i][0],get_wordnet_pos(tag[i][1])))
    lemmatized_Description = " ".join(lemmatized_list)
    return lemmatized_Description


def get_wordnet_pos(treebank_pos):

    if treebank_pos.startswith('J'):
        return wordnet.ADJ
    elif treebank_pos.startswith('V'):
        return wordnet.VERB
    elif treebank_pos.startswith('N'):
        return wordnet.NOUN
    elif treebank_pos.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
        #return ''        

        
def find_similarity(test_description_modified):
    ## make sparse array of filtered test description
    test_document_vector = vectorizer.transform([test_description_modified])
    test_document_encoded = (test_document_vector.toarray()) 

    #print (test_document_encoded)

    ## Cosine Similarity:

    all_documents_similarity = []
    ## all_documents_similarity is a array in whcih we save the similarity and the primary key/index together as we will have to sort the       list for selecting top similar descriptions, so we need to save the indexes as well
    for i in range(len(all_documents_encoded)):
        all_documents_similarity.append([cosine_similarity(all_documents_encoded[i],test_document_encoded), i])
        
        
#     ## Sort all similarities in desc order    
#     all_documents_similarity_sorted = sorted(all_documents_similarity, reverse = True) 

    ## Select similar documents:
    ## Select Top X% of the sorted values
    ## NOTE - Is there a better way to decide what percentage to select, other than trial and error on percentages?
    Xpercent = 0.15 ##Top 10 documents
    topXpercent = int(len(all_documents_similarity)*(Xpercent/100))
    
#     all_documents_similarity_sorted_topXpercent = all_documents_similarity_sorted[:topXpercent]
#     #print (all_documents_similarity)
#     #print (all_documents_similarity_sorted)
#     #print (topXpercent)
#     #print (all_documents_similarity_sorted_topXpercent)
    
   

    all_documents_similarity_sorted_topXpercent = sortTopXpercent(all_documents_similarity, topXpercent)
    
    
    print (all_documents_similarity_sorted_topXpercent[0][0][0][0])
    
    ## If highest similarity is < say 0.2 then tell the user to add more description for better results? - So as to tackle single word or       line descriptions. To tackle persistant users, add a button if they want analytics with only that much of description?
    if(all_documents_similarity_sorted_topXpercent[0][0][0][0] < 0.2):
        print ("For better analytics, enter more description specific to your app")

    ## Print index of the description found to be similar
    #print (all_documents_similarity_sorted_topXpercent[0][1])

    ## Link Datasets and Find Weighted Average of Ratings
    total_weight = 0
    total_weighted_rating = 0
    for i in range(len(all_documents_similarity_sorted_topXpercent)):
        #document_rating = data_full.iloc[(all_documents_similarity_sorted_topXpercent[i][1])]['user_rating']
        document_rating = rating_array[(all_documents_similarity_sorted_topXpercent[i][1])]
        if document_rating == 0:
            continue
        document_name = track_name_array[(all_documents_similarity_sorted_topXpercent[i][1])]
        document_id = all_documents_similarity_sorted_topXpercent[i][1]
        print (document_id, document_name, document_rating)
        document_weight = all_documents_similarity_sorted_topXpercent[i][0][0][0]
        document_weighted_rating = document_weight*document_rating
        total_weighted_rating = total_weighted_rating+document_weighted_rating
        total_weight = total_weight+document_weight

    final_rating = total_weighted_rating/total_weight
    return final_rating
   
        

        
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
           
        
        
        
        
        
print ("FILES LOADED", track_name_array[0])


start_time = time.time()

test_description = "Bank from almost anywhere with the Chase Mobile® app. Manage your accounts, pay bills, pay people, deposit checks, transfer money, all safely and securely with your device. Whether you’re on the go or curled up on the couch, day or night, with the Chase Mobile app, you’re in control of your accounts. CHECK YOUR ACCOUNT WITH JUST A FEW TAPS • Simply swipe to see your balances without signing in using Account Preview. • Sign in securely with fingerprint sign in and don’t worry about fat-fingering your password. • Monitor your checking, savings or credit card activities. • Keep track of your credit and debit card rewards that you’re saving for your next vacation. MANAGE YOUR ACCOUNTS WHEN YOU’RE ON THE GO • Set up a travel notification for your debit and credit cards to let us know if you’ll be away. • Opt in to Account Alerts and set your notification preferences so you can keep tabs on your account activity. MOVE MONEY WITHOUT STEPPING INSIDE A BRANCH • See how much you owe and when, plus schedule a payment for your Chase credit card, mortgage or other loan or line of credit. • Pay other bills such as utilities, service providers, and credit cards. • Use Chase QuickPay® with Zelle® to pay back your friends for lunch, your babysitter for the week or nudge your brother to pay you back for mom’s birthday gift. • Snap a picture and deposit checks with Chase QuickDeposit®. • Transfer money between your Chase accounts. • Reload your Chase Liquid® prepaid card. • Send wire transfers. CONNECT WITH CHASE • Find the nearest Chase branches and ATMs and get directions. • Speak with a service representative 24/7."
if detect(test_description) != 'en':
    print ("Error: Please enter plain english detailed description")
    exit()
else:
    ## POS Tagging and Lemmatization
    lemmatized_Description = lemmatizeDescription(test_description)
    print ("HI")

test_description_modified = lemmatized_Description
print (test_description_modified)


## SORT ONLY THOSE MUCH SIMILARITIES THAT ARE NEEDED - all_documents_similarity_sorted - dont sort all 7000 entires
## LSH HASHING - BUCKETS 8-10 
## Sklearn KNN
## WHAT IF WE REMOVE POS and LEMMATIZATION PART AND DIRECTLY PASS test_description in find_similarity()
## WHAT IF WE USE KNN instead of COSINE SIMILARITY
## WHAT IF WE REDUCE VOCAB SIZE TO 7000 or something like that - Text summarization? - Might decrease accuracy but also decrease running time

final_rating = find_similarity(test_description_modified)

print (final_rating)
print("--- %s seconds ---" % (time.time() - start_time))
