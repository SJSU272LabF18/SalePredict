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
## Load age group for each description
age_group_array = pickle.load(open("age_group.pickle", "rb"))
## Load All Documents Encoded Sparse Array npz file
## Load prime genre for each description
genre = pickle.load(open("genre.pickle", "rb"))

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
           
        
## For the graph of "number of users" by "Age Group" - 
def age_group_percent(users_by_ageGroup_dict, users_by_ageGroup_dict_percent, document_weight):
    for x in users_by_ageGroup_dict:
        temp3 = users_by_ageGroup_dict[x]
        users_by_ageGroup_dict[x] = int(temp3 + (document_weight*users_by_ageGroup_dict_percent[x]))
    return users_by_ageGroup_dict        

        
        
        
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
    users_by_ageGroup_dict = { "Children_5-13":0, "Teenager_13-18":0, "Adult_18-50":0, "Elderly_50+":0}
    total_users_that_rated = 0
    ## Arbitrary installs factor value, , through intuition - Apple dataset does not contain information about total installs so have to calculate an average value assuming that every 1 person among 'total_users_that_rated/installs_factor' number of persons rates the app
    installs_factor = 250
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
        
        
        total_users_that_rated = total_users_that_rated + document_weight
        
        
        ## For the graph of "number of users" by "Age Group" -  
        ## According to the 4 diff content ratings, we make 4 diff dict of percentages of usage for the 4 age groups
        ## Arbitrary average percentage values, through intuition- Apple dataset does not contain information about total user rating per age group or total installs per age group, for each app. Therefore we use arbitrary average values
        age_group = age_group_array[(all_documents_similarity_sorted_topXpercent[i][1])]
        if(age_group == "4+" or age_group == None or age_group == "0"):
            users_by_ageGroup_dict_percent = { "Children_5-13":0.05, "Teenager_13-18":0.25, "Adult_18-50":0.55, "Elderly_50+":0.15}
            users_by_ageGroup_dict = age_group_percent(users_by_ageGroup_dict, users_by_ageGroup_dict_percent, document_weight)     
        elif(age_group == "9+"):
            users_by_ageGroup_dict_percent = { "Children_5-13":0.03, "Teenager_13-18":0.27, "Adult_18-50":0.55, "Elderly_50+":0.15}
            users_by_ageGroup_dict = age_group_percent(users_by_ageGroup_dict, users_by_ageGroup_dict_percent, document_weight)        
        elif(age_group == "12+"): 
            users_by_ageGroup_dict_percent = { "Children_5-13":0.001, "Teenager_13-18":0.25, "Adult_18-50":0.599, "Elderly_50+":0.15}
            users_by_ageGroup_dict = age_group_percent(users_by_ageGroup_dict, users_by_ageGroup_dict_percent, document_weight)        
        elif(age_group == "17+"): 
            users_by_ageGroup_dict_percent = { "Children_5-13":0.0, "Teenager_13-18":0.05, "Adult_18-50":0.8, "Elderly_50+":0.15}
            users_by_ageGroup_dict = age_group_percent(users_by_ageGroup_dict, users_by_ageGroup_dict_percent, document_weight)
        
        #print ("users:", document_weight, "rating:", document_rating, "previous users at this rating:", users_at_this_rating, "new users at this rating", users_by_rating_dict[this_rating])
        print ("users:", document_weight, "rating:", document_rating, "Content rating:", age_group)
        
        print ("Current users_by_ageGroup_dict:", users_by_ageGroup_dict)
        
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
    
    ## Total predicted installs
    factor = total_users_that_rated/installs_factor
    print("Total installs: ", int(total_users_that_rated*factor))
    
    ## Total predicted "users that rated" ordered by age
    print ("Users that rated, ordered by age:", users_by_ageGroup_dict)
    
    ## Total predicted "installs" ordered by age 
    for x in users_by_ageGroup_dict:
        temp4 = users_by_ageGroup_dict[x]
        users_by_ageGroup_dict[x] = temp4*factor
    print ("Installs, ordered by age:", users_by_ageGroup_dict)
    
    ## Print genre as the genre of the description with the highest similarity
    prime_genre = genre[all_documents_similarity_sorted_topXpercent[0][1]]
    print("Prime Genre: ", prime_genre)
    
    return final_rating
   
        

        
        
        
print ("FILES LOADED")


start_time = time.time()

test_description = "With 30 billion matches to date, Tinder® is the world’s most popular app for meeting new people. Think of us as your most dependable wingmate—wherever you go, we’ll be there. If you’re here to meet new people, expand your social network, meet locals when you’re traveling, or just live in the now, you’ve come to the right place. We’re called “the world’s hottest app” for a reason: we spark more than 26 million matches per day. How many dating apps do that? Match. Chat. Date. Tinder is easy and fun—use the Swipe Right™ feature to Like someone, use the Swipe Left™ feature to pass. If someone likes you back, It’s a Match! We invented the double opt-in so that two people will only match when there’s a mutual interest. No stress. No rejection. Just tap through the profiles you’re interested in, chat online with your matches, then step away from your phone, meet up in the real world and spark something new. Now, let’s get started. And remember, when in doubt, Swipe Right. Trust us, the more options you have, the better-looking life becomes. Welcome to Tinder—the largest, hottest community of singles in the world. Don’t be shy, come on over. MORE FEATURES? THAT’S A PLUS Upgrade to Tinder Plus® for premium features, including: Unlimited Likes so you can use the Swipe Right feature to your heart’s content, Passport to chat with singles anywhere around the world, Rewind to give someone a second chance, one free Boost per month to be the top profile in your area for 30 minutes, and additional Super Likes to stand out from the crowd. GET THE GOLD TREATMENT Upgrade to Tinder Gold™ for a first-class experience: Passport, Rewind, Unlimited Likes, five Super Likes per day, one Boost per month, and more profile controls. But wait, it gets better. Save time and aimless searching with our Likes You feature, which lets you see who likes you. Think of it as your personal Tinder concierge—available 24/7—bringing all of your pending matches to you. Now you can sit back, enjoy a fine cocktail, and browse through profiles at your leisure. Goodbye search fatigue. Hello #GoldLife ----------------------------------- If you choose to purchase Tinder Plus or Tinder Gold, payment will be charged to your Google Play account, and your account will be charged for renewal within 24-hours prior to the end of the current period. Auto-renewal may be turned off at any time by going to your settings in the Play Store after purchase. Current Tinder Plus subscription price starts at $9.99 USD/month, and one-month, 6-month and 12-month packages are available. Current Tinder Gold subscription price starts at $14.99 USD/month, and one-month, 6-month and 12-month packages are available. Prices are in U.S. dollars, may vary in countries other than the U.S. and are subject to change without notice. No cancellation of the current subscription is allowed during the active subscription period. If you don’t choose to purchase Tinder Plus or Tinder Gold, you can simply continue using Tinder for free"


if detect(test_description) != 'en':
    print ("Error: Please enter plain english detailed description")
    exit()
else:
    ## POS Tagging and Lemmatization
    lemmatized_Description = lemmatizeDescription(test_description)
    print ("HI")

test_description_modified = lemmatized_Description
#print (test_description_modified)


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
#### Pie Chart of users by age group
### All pages:
#### show top 3 apps similar and their description excript (most important text summarized?) and their similarity percentage, and their number of installs
#### For more detailed analysis - sign up/login and premium
#### Top 3 Free or paid? whether you should put a prize on your app?


## To Do:
## Find such description that will have average rating less than 3.0
