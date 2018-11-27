from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text
#import numpy as np
import pandas as pd ## Read and manipulate csv
from langdetect import detect ## Detect Language
import pickle ## pickle the model

''' NOTE - # is Commented Code and ## is just Comment and ### is Sub-Comment for the nearest ## above'''
## NOTE - Refer 'sklearn_model_dummy' file for full description of methodology and functions used

## Reading from csv using pandas
path = 'C:\\Users\\shrke\\Desktop\\272 Project\\Apple store dataset\\'
data_full = pd.read_csv(path + "AppleStore.csv")
## Show top 5 rows in dataset
#data_full.head()

path = 'C:\\Users\\shrke\\Desktop\\272 Project\\Apple store dataset\\'
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

print (description_array[0])        


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
test_description = "SAVE 20%, now only $3.99 for a limited time! One of the most popular video games in arcade history! 2015 World Video Game Hall of Fame Inductee Who can forget the countless hours and quarters spent outrunning pesky ghosts and chompin’ on dots? Now you can have the same arcade excitement on your mobile devices! Guide PAC-MAN through the mazes with easy swipe controls, a MFi controller, or kick it old school with the onscreen joystick! Eat all of the dots to advance to the next stage. Go for high scores and higher levels! Gain an extra life at 10.000 points! Gobble Power Pellets to weaken ghosts temporarily and eat them up before they change back. Avoid Blinky, the leader of the ghosts, and his fellow ghosts Pinky, Inky, and Clyde, or you will lose a life. It’s game over when you lose all your lives. 9 NEW MAZES Included!!! The game includes 9 new mazes in addition to the pixel for pixel recreation of the classic original maze. Challenge your skill to beat them all! We are constantly updating the game with new maze packs that you can buy to complete your PAC-MAN collection. HINTS and TIPS!!! Insider pro-tips and hints are being made available for the first time in-game! Use these to help you become a PAC-MAN champion! FEATURES: • New tournaments • New Visual Hints and Pro-tips • New mazes for all new challenges • Play an arcade perfect port of classic PAC-MAN • Two different control modes • Three game difficulties (including the original 1980 arcade game) • Retina display support • MFi controller support"
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

## Hosting the Model: 2 Approaches: 1) Pickle model 2) REST API
## https://stackoverflow.com/questions/49216223/integration-of-python-ml-model-with-a-web-application

## Going forward with approach 2:
## Pickling the File
## Refer - https://wiki.python.org/moin/UsingPickle
## Refer - https://pythontips.com/2013/08/02/what-is-pickle-in-python/
## Use pickle (python) or cpickle (c)? cpickle is faster than pickle
## In Python 2, you can speed up your pickle access with cPickle. (In Python3, importing pickle will automatically use the accelerated version if it is available.)

pickle_input = all_documents_encoded
pickle.dump(pickle_input, open("pickle_input.pickle", "wb"))
pickle_output = pickle.load(open("pickle_input.pickle", "rb"))
#pickle_output[0]

## if pickle load takes time then can we put all_documents_encoded into a text file and load that when needed? WOuld theat be faster?
## At the end of the notebook link the next notebook

values = pickle_input

with open("test.txt", "w") as output:
    output.write(str(values)) 
    
with open('test.txt', 'r') as myfile:
    data=myfile.read().replace('\n', '')
    
data[0]

## NOTE - pipeline, one function/api to run/load the prediction?
