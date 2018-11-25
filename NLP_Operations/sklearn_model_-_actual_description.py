from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text
#import numpy as np
import pandas as pd ## Read and manipulate csv
from langdetect import detect ## Detect Language

''' NOTE - # is Commented Code and ## is just Comment and ### is Sub-Comment for the nearest ## above'''
## NOTE - Refer 'sklearn_model_-_dummy_description' file for full description of methodology and functions used

## Reading from csv using pandas
path = 'C:\\Users\\shrke\\Desktop\\272 Project\\Dataset\\'
data_full = pd.read_csv(path + "AppleStore.csv")
## Show top 5 rows in dataset
#data_full.head()

path = 'C:\\Users\\shrke\\Desktop\\272 Project\\Dataset\\'
data_desc = pd.read_csv(path + "appleStore_description.csv")

## List column headers
#list(data_desc)
## List all under column header 'id'
#print (data_desc['id'])

'''
##Checking if any track_name under data_full is not aligned with track_name under data_desc, for the same id
for i in range(len(data_full)):
    ## print each element under track_name column
    #print(data_full.iloc[i]['track_name'])
    if data_full.iloc[i]['track_name'] != data_desc.iloc[i]['track_name']:
        print("Mismatch:", i, data_full.iloc[i]['track_name'])
'''

description_array = []
## Array that stores all descriptions

## Check Non-English data  
#print (description_array[403])
## Refer - 'translate_non_-_english_descriptions' for translation functions. 
## The translation functions have error and therefore translation is not an option
## Therefore we can either remove the non-english descriptions with storing in description_array or we can let it stay as it is
## Note that vectorizer.vocabulary_ also counts the non-english words in vocab. But this does not effect the end result as the test description would be in english and so the non-enlish vocab words do not affect in finding similar descriptions 

## Append all descriptions into a single array
## Removing the non-english descriptions and keeping them as " " i.e empty strings. Note that even after applying this filter, some non-english words were still in the vocabulary due to unknown reason
for i in range(len(data_full)):  
    ## Detect language of current description
    if detect(data_desc.iloc[i]['app_desc']) != 'en':
        description_array.append(" ")
    else:
        ## Append the app_desc present in row i, to description_array at i index
        description_array.append(data_desc.iloc[i]['app_desc'])

## create the transform
vectorizer = TfidfVectorizer(stop_words = 'english')   

## tokenize and build vocabulary
vectorizer.fit(description_array)

## print vocabulary
#print(vectorizer.vocabulary_)
#print(vectorizer.idf_)

## encode each document and save in a combined array
all_documents_encoded = []
for i in range(len(description_array)):
    vector = vectorizer.transform([description_array[i]]) ## make sparse array
    ## summarize encoded vector
    all_documents_encoded.append(vector.toarray())  
    
#print (all_documents_encoded[0])

## Words in vocabulary
#print(len(vectorizer.vocabulary_))  

## print the range of a document vector
print(vector.shape)


## Test Description - Tokenization and Filteration:
test_description = "Netflix is the world’s leading subscription service for watching TV episodes and films on your phone. This Netflix mobile application delivers the best experience anywhere, anytime. Get the free app as a part of your Netflix membership and you can instantly watch thousands of TV episodes & films on your phone. If you are not a Netflix member sign up for Netflix and start enjoying immediately on your phone with our one-month free trial. How does Netflix work? • Netflix membership gives you access to unlimited TV programmes and films for one low monthly price. • With the Netflix app you can instantly watch as many TV episodes & films as you want, as often as you want, anytime you want. • You can Browse a growing selection of thousands of titles, and new episodes that are added regularly. • Search for titles and watch immediately on your phone or on an ever expanding list of supported devices. • Rate your favorite programmes and films and tell us what you like so Netflix can help suggest the best titles for you. • Start watching on one device, and resume watching on another. Check out netflix.com for all the TVs, game consoles, tablets, phones, Blu-ray players and set top boxes on which you can watch Netflix."
tokenizer = vectorizer.build_tokenizer()
test_description_tokens = tokenizer(test_description)
#print (test_description_tokens)   

## Store all words from sklearn stop words file
stop_words = text.ENGLISH_STOP_WORDS

test_description_tokens_filtered = []
for i in range(len(test_description_tokens)):
    ## if the current token lowercased is not in stop words and is present in vocabulary, then append the token to a token array
    if not test_description_tokens[i].lower() in stop_words and vectorizer.vocabulary_.get(test_description_tokens[i].lower()) != None :
        test_description_tokens_filtered.append(test_description_tokens[i].lower())

#print (test_description_tokens_filtered)

# Join tokens to form the filtered test description string
test_description_modified = " ".join(test_description_tokens_filtered)

## make sparse array of filtered test description
test_document_vector = vectorizer.transform([test_description_modified])
test_document_encoded = (test_document_vector.toarray()) 

print (test_document_encoded)

## Cosine Similarity:

all_documents_similarity = []
## all_documents_similarity is a array in whcih we save the similarity and the primary key/index together as we will have to sort the list for selecting top similar descriptions, so we need to save the indexes as well
for i in range(len(all_documents_encoded)):
    all_documents_similarity.append([cosine_similarity(all_documents_encoded[i],test_document_encoded), i])

## Sort all similarities in desc order    
all_documents_similarity_sorted = sorted(all_documents_similarity, reverse = True) 

## Select similar documents:
## Select Top X% of the sorted values
## NOTE - Is there a better way to decide what percentage to select, other than trial and error on percentages?
Xpercent = 0.15 ##Top 10 documents
topXpercent = int(len(all_documents_similarity_sorted)*(Xpercent/100))
all_documents_similarity_sorted_topXpercent = all_documents_similarity_sorted[:topXpercent]
#print (all_documents_similarity)
#print (all_documents_similarity_sorted)
print (topXpercent)
print (all_documents_similarity_sorted_topXpercent)

## If highest similarity is < say 0.2 then tell the user to add more description for better results? - So as to tackle single word or line descriptions. To tackle persistant users, add a button if they want analytics with only that much of description?
if(all_documents_similarity_sorted_topXpercent[0][0][0][0] < 0.2):
    print ("For better analytics, enter more description specific to your app")
    
## Print index of the description found to be similar
#print (all_documents_similarity_sorted_topXpercent[0][1])

## Link Datasets and Find Weighted Average of Ratings
total_weight = 0
total_weighted_rating = 0
for i in range(len(all_documents_similarity_sorted_topXpercent)):
    document_rating = data_full.iloc[(all_documents_similarity_sorted_topXpercent[i][1])]['user_rating']
    if document_rating == 0:
        continue
    document_name = data_full.iloc[(all_documents_similarity_sorted_topXpercent[i][1])]['track_name']
    document_id = all_documents_similarity_sorted_topXpercent[i][1]
    print (document_id, document_name, document_rating)
    document_weight = all_documents_similarity_sorted_topXpercent[i][0][0][0]
    document_weighted_rating = document_weight*document_rating
    total_weighted_rating = total_weighted_rating+document_weighted_rating
    total_weight = total_weight+document_weight
    
final_rating = total_weighted_rating/total_weight
print (final_rating)  
