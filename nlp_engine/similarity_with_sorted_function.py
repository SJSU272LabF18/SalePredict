## to compare runtime with manual topX sort
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
## create the transform
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
        
        
        
    ## Select similar documents:
    ## Select Top X% of the sorted values
    ## NOTE - Is there a better way to decide what percentage to select, other than trial and error on percentages?
    Xpercent = 0.15 ##Top 10 documents
    topXpercent = int(len(all_documents_similarity)*(Xpercent/100)) 
    
    
    
    ## Sort all similarities in desc order    
    all_documents_similarity_sorted_topXpercent_index = sorted(range(len(all_documents_similarity)), key=lambda i: all_documents_similarity[i]) [-topXpercent:]
    ## Refer - https://stackoverflow.com/questions/13070461/get-index-of-the-top-n-values-of-a-list-in-python
    
    all_documents_similarity_sorted_topXpercent = []
    for i in range(len(all_documents_similarity_sorted_topXpercent_index)):
        all_documents_similarity_sorted_topXpercent.append(all_documents_similarity[all_documents_similarity_sorted_topXpercent_index[i]][0][0])
#     #print (all_documents_similarity)
#     #print (all_documents_similarity_sorted)
#     #print (topXpercent)
#     #print (all_documents_similarity_sorted_topXpercent)

    
    
    
#     ## If highest similarity is < say 0.2 then tell the user to add more description for better results? - So as to tackle single word or       line descriptions. To tackle persistant users, add a button if they want analytics with only that much of description?
#     if(all_documents_similarity_sorted_topXpercent[len(all_documents_similarity_sorted_topXpercent)-1] < 0.2):
#         print ("For better analytics, enter more description specific to your app")

    ## Print index of the description found to be similar
    #print (all_documents_similarity_sorted_topXpercent[0][1])

    ## Link Datasets and Find Weighted Average of Ratings
    total_weight = 0
    total_weighted_rating = 0
    for i in range(len(all_documents_similarity_sorted_topXpercent)):
        #document_rating = data_full.iloc[(all_documents_similarity_sorted_topXpercent[i][1])]['user_rating']
        document_rating = rating_array[(all_documents_similarity_sorted_topXpercent_index[i])]
        if document_rating == 0:
            continue
        document_name = track_name_array[(all_documents_similarity_sorted_topXpercent_index[i])]
        document_id = all_documents_similarity_sorted_topXpercent_index[i]
        print (document_id, document_name, document_rating)
        document_weight = all_documents_similarity_sorted_topXpercent[i]
        print (document_weight)
        document_weighted_rating = document_weight*document_rating
        total_weighted_rating = total_weighted_rating+document_weighted_rating
        total_weight = total_weight+document_weight

    final_rating = total_weighted_rating/total_weight
    return final_rating
   
        
        
        
        
        
print ("FILES LOADED", track_name_array[0])




start_time = time.time()

test_description = "WhatsApp Messenger is a FREE messaging app available for Android and other smartphones. WhatsApp uses your phone's Internet connection (4G/3G/2G/EDGE or Wi-Fi, as available) to let you message and call friends and family. Switch from SMS to WhatsApp to send and receive messages, calls, photos, videos, documents, and Voice Messages. WHY USE WHATSAPP: • NO FEES: WhatsApp uses your phone's Internet connection (4G/3G/2G/EDGE or Wi-Fi, as available) to let you message and call friends and family, so you don't have to pay for every message or call.* There are no subscription fees to use WhatsApp. • MULTIMEDIA: Send and receive photos, videos, documents, and Voice Messages. • FREE CALLS: Call your friends and family for free with WhatsApp Calling, even if they're in another country.* WhatsApp calls use your phone's Internet connection rather than your cellular plan's voice minutes. (Note: Data charges may apply. Contact your provider for details. Also, you can't access 911 and other emergency service numbers through WhatsApp). • GROUP CHAT: Enjoy group chats with your contacts so you can easily stay in touch with your friends or family. • WHATSAPP WEB: You can also send and receive WhatsApp messages right from your computer's browser. • NO INTERNATIONAL CHARGES: There's no extra charge to send WhatsApp messages internationally. Chat with your friends around the world and avoid international SMS charges.* • SAY NO TO USERNAMES AND PINS: Why bother having to remember yet another username or PIN? WhatsApp works with your phone number, just like SMS, and integrates seamlessly with your phone's existing address book. • ALWAYS LOGGED IN: With WhatsApp, you're always logged in so you don't miss messages. No more confusion about whether you're logged in or logged out. • QUICKLY CONNECT WITH YOUR CONTACTS: Your address book is used to quickly and easily connect you with your contacts who have WhatsApp so there's no need to add hard-to-remember usernames. • OFFLINE MESSAGES: Even if you miss your notifications or turn off your phone, WhatsApp will save your recent messages until the next time you use the app. • AND MUCH MORE: Share your location, exchange contacts, set custom wallpapers and notification sounds, email chat history, broadcast messages to multiple contacts at once, and more! *Data charges may apply. Contact your provider for details."

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
