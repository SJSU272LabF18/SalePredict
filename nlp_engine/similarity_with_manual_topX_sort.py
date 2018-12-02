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
## Load rating count for each description
rating_count_array = pickle.load(open("rating_count_tot.pickle", "rb"))
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
    
   
    ## SORT ONLY THOSE MUCH SIMILARITIES THAT ARE NEEDED - all_documents_similarity_sorted - dont sort all 7000 or so entires - Sort only to get the topXpercent similarity values
    all_documents_similarity_sorted_topXpercent = sortTopXpercent(all_documents_similarity, topXpercent)
    
    
    print (all_documents_similarity_sorted_topXpercent[0][0][0][0])
    
    ## If highest similarity is < say 0.2 then tell the user to add more description for better results? - So as to tackle single word or       line descriptions. To tackle persistant users, add a button if they want analytics with only that much of description?
    if(all_documents_similarity_sorted_topXpercent[0][0][0][0] < 0.35):
        print ("For better analytics, enter more description specific to your app idea")

    ## Print index of the description found to be similar
    #print (all_documents_similarity_sorted_topXpercent[0][1])

    ## Link Datasets and Find Weighted Average of Ratings and other details
    total_weight = 0
    total_weighted_rating = 0
    users_by_rating_dict = { "0.5":0, "1.0":0, "1.5":0, "2.0":0, "2.5":0, "3.0":0, "3.5":0, "4.0":0, "4.5":0, "5.0":0 }
    total_users_that_rated = 0
    for i in range(len(all_documents_similarity_sorted_topXpercent)):
        #document_rating = data_full.iloc[(all_documents_similarity_sorted_topXpercent[i][1])]['user_rating']
        document_rating = rating_array[(all_documents_similarity_sorted_topXpercent[i][1])]
        document_rating_count = rating_count_array[(all_documents_similarity_sorted_topXpercent[i][1])]
        if document_rating_count == 0:
            continue
        if document_rating == 0:
            continue
        document_name = track_name_array[(all_documents_similarity_sorted_topXpercent[i][1])]
        document_id = all_documents_similarity_sorted_topXpercent[i][1]
        print ("id:",document_id, "name:", document_name, "rating:", document_rating, "rating_count:", document_rating_count, "similarity:", all_documents_similarity_sorted_topXpercent[i][0][0][0])
        
        ## Find the final Average rating - Weighted average of ratings of topXpercent similar documents 
        ## Considering Document weight = Similarity Score multiplied by document_rating_count
        document_weight = all_documents_similarity_sorted_topXpercent[i][0][0][0]*document_rating_count
        document_weighted_rating = document_weight*document_rating
        total_weighted_rating = total_weighted_rating+document_weighted_rating
        total_weight = total_weight+document_weight
        
        ## For the graph of "number of users" by "Rating Given" - 
        this_rating = str(document_rating)
        users_at_this_rating = users_by_rating_dict[this_rating]
        users_by_rating_dict[this_rating] = int(users_at_this_rating + document_weight)
        print ("users:", document_weight, "rating:", document_rating, "previous users at this rating:", users_at_this_rating, "new users at this rating", users_by_rating_dict[this_rating])
        total_users_that_rated = total_users_that_rated + document_weight
        
        
    ## Final Average rating    
    final_rating = total_weighted_rating/total_weight
    
    
    ## Total users by rating (dictionary)
    print("Users by rating:", users_by_rating_dict)
    ## Note here that this dictionary is not normalized, i.e it could be possible that:
    ## Consider the following final dictionary - Users by rating: {'0.5': 0, '1.0': 0, '1.5': 0, '2.0': 0, '2.5': 0, '3.0': 503946, '3.5': 0, '4.0': 27265, '4.5': 9559, '5.0': 0}
    ## There are no users at rating 0.5, 1.0, and so on which will not give a distributed graph
    ## Therefore we equalize the graph to some extent so that the peaks get distributed and we get a smoother bar graph (This is possibly manipulation of dataset but the kaggle dataset does not have user count for each rating increment for any particular distribution, and that's why we have to normalize the graph)    
    ## For this we need total_users_that_rated as the total number of ratings given
    print("Total users that are likely to rate: ", int(total_users_that_rated))
    ## NOTE - Could not find a library for this so make a function for equalization?
    
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

test_description = "SAVE 20%, now only $3.99 for a limited time! One of the most popular video games in arcade history! 2015 World Video Game Hall of Fame Inductee Who can forget the countless hours and quarters spent outrunning pesky ghosts and chompinâ€™ on dots? Now you can have the same arcade excitement on your mobile devices! Guide PAC-MAN through the mazes with easy swipe controls, a MFi controller, or kick it old school with the onscreen joystick! Eat all of the dots to advance to the next stage. Go for high scores and higher levels! Gain an extra life at 10.000 points! Gobble Power Pellets to weaken ghosts temporarily and eat them up before they change back. Avoid Blinky, the leader of the ghosts, and his fellow ghosts Pinky, Inky, and Clyde, or you will lose a life. Itâ€™s game over when you lose all your lives. 9 NEW MAZES Included!!! The game includes 9 new mazes in addition to the pixel for pixel recreation of the classic original maze. Challenge your skill to beat them all! We are constantly updating the game with new maze packs that you can buy to complete your PAC-MAN collection. HINTS and TIPS!!! Insider pro-tips and hints are being made available for the first time in-game! Use these to help you become a PAC-MAN champion! FEATURES: â€¢ New tournaments â€¢ New Visual Hints and Pro-tips â€¢ New mazes for all new challenges â€¢ Play an arcade perfect port of classic PAC-MAN â€¢ Two different control modes â€¢ Three game difficulties (including the original 1980 arcade game) â€¢ Retina display support â€¢ MFi controller support"

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
if (final_rating >= 3): 
    print ("SUCCESS")
else:
    print ("FAILURE")
print("--- %s seconds ---" % (time.time() - start_time))

## Frontend display:
### Page 1:
#### Show success or failure
#### show average rating rounded off
#### Show your pecentile/ranking w.r.t all other apps in the app store. And w.r.t genre as well?
#### Show genre of app?
#### Show potential number of total installs
#### Show potential number of total users that will rate
### Page 2:
#### show graph of number of users by rating
### Page 3:
#### 
### All pages:
#### show top 3 apps similar and their description excript (most important text summarized?) and their similarity percentage, and their number of installs
#### For more detailed analysis - sign up/login and premium
#### Top 3 Free or paid? whether you should put a prize on your app?


## To Do:
## Find such description that will have average rating less than 3.0
