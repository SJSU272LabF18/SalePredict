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

import scipy.sparse

# import numpy
# numpy.set_printoptions(threshold=numpy.nan) ## To print the full NumPy array when jupyter notebook truncates the stdout with ... in between

''' NOTE - # is Commented Code and ## is just Comment and ### is Sub-Comment for the nearest ## above'''
## NOTE - Refer 'sklearn_model_dummy' file for full description of methodology and functions used

## Reading from csv using pandas
path_dataset = 'C:\\Users\\shrke\\Desktop\\272 Project\\Apple store dataset\\'
data_full = pd.read_csv(path_dataset + "AppleStore.csv")
## Show top 5 rows in dataset
#data_full.head()

data_desc = pd.read_csv(path_dataset + "appleStore_description.csv")


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


## POS Tagging and Lemmatization function      
## See 'pos_tagging_and_lemmatization' file full explanation       
regexp_tokenizer = RegexpTokenizer(r'\w+')        
def lemmatizeDescription(current_description):
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
        ## POS Tagging and Lemmatization
        lemmatized_Description = lemmatizeDescription(data_desc.iloc[i]['app_desc'])
        ## Append the app_desc present in row i, to description_array at i index   
        description_array.append(lemmatized_Description)

## description_array stores at each index the corresponding description. This index is very important as it matches the description to other features of the app from the csv file
## NOTE - this index and the "id" column from csv file are different  

# print (description_array[0])
# print (description_array[7196])

## create the transform
## Only top k words are put into vocab as max_features = k (top according to their frequency)
## NOTE - This humongously improves similarity finding time as we reduce total vocab from about 40000 to about 10000. There might be some tradeoff with the similarity finding accuracy but it is satisfactory in our use case
vectorizer = TfidfVectorizer(stop_words = 'english', max_features = 9500)   

## tokenize and build vocabulary
vectorizer.fit(description_array)

## To reduce the vocabulary and remove the words that occur very infrequently accross the descriptions, we sort the idf array and then print top k elements to see where to put the limit so as to not include any words below this limit
## This k shall be put as max_feature in TfidfVectorizer
# import numpy as np

# indices = np.argsort(vectorizer.idf_)[::-1]
# features = vectorizer.get_feature_names()
# print (len(features))
# bottom_n = 0
# top_features = [features[i] for i in indices[bottom_n:]]
# print (top_features)

# ## Refer - https://stackoverflow.com/questions/25217510/how-to-see-top-n-entries-of-term-document-matrix-after-tfidf-in-scikit-learn/25219535
# ## Refer - https://stackoverflow.com/questions/46118910/scikit-learn-vectorizer-max-features

#print vocabulary
#print(vectorizer.vocabulary_)
#print(vectorizer.idf_)

## encode each document and save in a combined array
all_documents_encoded = []
for i in range(len(description_array)):
    vector = vectorizer.transform([description_array[i]]) ## make sparse array
    ## summarize encoded vector
    vector_array = vector.toarray()
    all_documents_encoded.append(vector_array[0]) 
    
## Words in vocabulary
#print(len(vectorizer.vocabulary_))  

## print the range of a document vector
print(vector.shape)
#print(all_documents_encoded[0])


sparse_matrix = scipy.sparse.csc_matrix(all_documents_encoded)
sparse_matrix.todense()

path_trained_model = 'trained_model_-_pickle_and_np_sparse_files\\'

scipy.sparse.save_npz(path_trained_model + 'sparse_matrix_actual.npz', sparse_matrix)

sparse_matrix = scipy.sparse.load_npz(path_trained_model + 'sparse_matrix_actual.npz')
sparse_matrix = sparse_matrix.todense()

print (sparse_matrix[7196])
all_documents_encoded = sparse_matrix

'''
## Test Description - Tokenization and Filteration with sklearn - With no POS tagging & Lemmatization: 
test_description = "REAL OFF-ROADING MISSIONS Inspired by the real rules of Off Road Driving Competitions, can you navigate every mission without getting any penalties to get a Gold Medal for every event? Youâ€™ll need to pass through the gates carefully because hitting flags, stopping or reversing all give a penalty score. Youâ€™re not against the clock here, so take your time and drive with precision. Get a perfect clean run for those elusive Gold Medals!! Get ready for the ULTIMATE Off Road Driving Simulator Experience! GAME FEATURES â–¶ 10 Epic Off-Road 4x4 Trucks, Buggies, SUVâ€™s & Pickups â–¶ 50 Amazing All-Terrain Trials Driving Missions â–¶ Real Off Road Competition Rules â–¶ Beautiful Realistic Forest to Explore â–¶ Ultra-Realistic Terrain Details â–¶ Driving Challenges designed to put your Skills to the Test â–¶ 100% Free-2-Play, with No Strings Attached â–¶ iCloud Support. Continue progress on your other devices! â–¶ Runs on anything from (or better than) the iPhone 4, iPad 2, iPad Mini & iPod Touch (5th Generation) OUR FREE TO PLAY PROMISE The Main Game Mode is 100% FREE to Play, all the way through, no strings attached! Extra Game Modes that alter the rules slightly to make the game easier are available through In-App Purchases."
sklearn_tokenizer = vectorizer.build_tokenizer()
test_description_tokens = sklearn_tokenizer(test_description)
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
'''


## Test Description - Pos tagging and lemmatization with nltk:
test_description = "5 previous escape games plus 1 new game in one package!  The Cupcake Shop  is the 11th escape game produced by FUNKYLAND. This special package includes the new game,  Cupcake Shop  and 5 previous escape games (Cake CafÃ©, Ice Cream Parlor, Fruit Juice Parlor, Halloween Candy Shop, and Crepe House). You can choose to play your favorite of 6 charming and easy escape games. Find the items and solve the mysteries to escape from each shop. How to Play: - Just tap - Tap the item icon twice to enlarge the display. - Tap the [+] button in the upper right hand corner to display the settings screen. Game Features: - Beautiful graphics - Auto-save - Easy and fun, even for those not keen on escape games - Perfect game length to kill time The Save Function: The game auto-saves items you've acquired and instruments you've unlocked, allowing you to restart at the last auto-save checkpoint. In case you can't restart, please check your device settings as there may not be enough storage space. The list of shops: Cupcake Shop << New!! Cake CafÃ© Ice Cream Parlor Fruit Juice Parlor Halloween Candy Shop Crepe House"
if detect(test_description) != 'en':
    print("Please enter the description in plain english.")
else:
    ## POS Tagging and Lemmatization
    lemmatized_Description = lemmatizeDescription(test_description)
    
test_description_modified = lemmatized_Description

## make sparse array of filtered test description
test_document_vector = vectorizer.transform([test_description_modified])
test_document_encoded = (test_document_vector.toarray()) 

#print (test_document_encoded)

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

## Hosting the Model: 
## Flask server hosts the encoded sparse array (trained model), and recieves the string description from node.js as json. String is converted into the vector and then similarity is found out and result is generated in flask and sent to node.js as json.
## https://stackoverflow.com/questions/49216223/integration-of-python-ml-model-with-a-web-application

## 2 Approaches for saving the trained model on disk. The saved file will be hosted on server: 
## 1) Pickle the sparse array file 2) Convert the sparse array into scipy.sparse.csc_matrix which only stores the array elements that are not zero, and their locations

'''
## Pickling the File
## Refer - https://wiki.python.org/moin/UsingPickle
## Refer - https://pythontips.com/2013/08/02/what-is-pickle-in-python/
## Use pickle (python) or cpickle (c)? cpickle is faster than pickle
## In Python 2, you can speed up your pickle access with cPickle. (In Python3, importing pickle will automatically use the accelerated version if it is available.)

pickle_input = all_documents_encoded
pickle.dump(pickle_input, open("pickle_input.pickle", "wb"))
pickle_output = pickle.load(open("pickle_input.pickle", "rb"))
#pickle_output[0]

### Instead of pickling, saving the sparse matrix into a text file?
### ## if pickle load takes time then can we put all_documents_encoded into a text file and load that when needed? WOuld theat be faster?
### ## At the end of the notebook link the next notebook
### values = pickle_input
### with open("test.txt", "w") as output:
###     output.write(str(values))
### with open('test.txt', 'r') as myfile:
###     data=myfile.read().replace('\n', '')    
### data[0]

## Pickled file is about 2 GB large which is not good as we have to load this file into cloud and also un-pickle it when server starts which will take time as it is big
## Therefore, saving sparse matrix as SciPy CSC Sparse Matrix .npz (numpy) is a much better option for our use case. This file is around 6 MB, which is an immense improvement
## Note that, pickling is generally used to store complex trained model. Sparse matrix is not complex therefore no need for pickling
'''

## Going forward with approach 2:
## Scipy sparse matrix - Refer 'save_sparse_matrix_dummy' file

## NOTE - pipeline, one function/api to run/load the prediction?

## Pickle description_array 
description_array[0]

pickle_input = description_array
pickle.dump(pickle_input, open(path_trained_model + "description_array.pickle", "wb"))
pickle_output = pickle.load(open(path_trained_model + "description_array.pickle", "rb"))
pickle_output[1]

pickle_output[7196]

# import pandas as pd
# import pickle ## pickle the model

# ## Reading from csv using pandas
# path_dataset = 'C:\\Users\\shrke\\Desktop\\272 Project\\Apple store dataset\\'
# data_full = pd.read_csv(path_dataset + "AppleStore.csv")

rating_array = [] 
## Array that stores all ratings
for i in range(len(data_full)):
    current_rating = data_full.iloc[i]['user_rating']
    if(current_rating >= 0.0 and current_rating <= 5.0): 
        rating_array.append(current_rating)
    else: 
        current_rating = 0.0
        rating_array.append(current_rating)
        
#rating_array[7196]

pickle_input = rating_array
pickle.dump(pickle_input, open(path_trained_model + "rating_array.pickle", "wb"))
pickle_output = pickle.load(open(path_trained_model + "rating_array.pickle", "rb"))
pickle_output[0]

track_name_array = [] 
## Array that stores all ratings
for i in range(len(data_full)):
    track_name_array.append(data_full.iloc[i]['track_name'])
    
#track_name_array[0]

pickle_input = track_name_array
pickle.dump(pickle_input, open(path_trained_model + "track_name_array.pickle", "wb"))
pickle_output = pickle.load(open(path_trained_model + "track_name_array.pickle", "rb"))
pickle_output[0]

rating_count_tot = [] 
## Array that stores all number of ratings
for i in range(len(data_full)):
    rating_count_tot.append(data_full.iloc[i]['rating_count_tot'])

    
pickle_input = rating_count_tot
pickle.dump(pickle_input, open(path_trained_model + "rating_count_tot.pickle", "wb"))
pickle_output = pickle.load(open(path_trained_model + "rating_count_tot.pickle", "rb"))
pickle_output[0]

age_group = [] 
## Array that stores all content rating
for i in range(len(data_full)):
    age_group.append(data_full.iloc[i]['cont_rating'])
    

pickle_input = age_group
pickle.dump(pickle_input, open(path_trained_model + "age_group.pickle", "wb"))
pickle_output = pickle.load(open(path_trained_model + "age_group.pickle", "rb"))
pickle_output[0]

genre = [] 
## Array that stores all prime genre
for i in range(len(data_full)):
    genre.append(data_full.iloc[i]['prime_genre'])
    
pickle_input = genre
pickle.dump(pickle_input, open(path_trained_model + "genre.pickle", "wb"))
pickle_output = pickle.load(open(path_trained_model + "genre.pickle", "rb"))
pickle_output[0]

## Append all descriptions as it is from dataset, into a single array 
## Removing the non-english descriptions and keeping them as " " i.e empty strings. Note that even after applying this filter, some non-english words were still in the vocabulary due to unknown reason
## To show 2-3 lines of the unmodified app description of top 3 similar apps
unmodified_description_array = []
for i in range(len(data_full)):  
    ## Detect language of current description
    if detect(data_desc.iloc[i]['app_desc']) != 'en':
        unmodified_description_array.append(" ")
    else:
        unmodified_description_array.append(data_desc.iloc[i]['app_desc'])
        
pickle_input = unmodified_description_array
pickle.dump(pickle_input, open(path_trained_model + "unmodified_description_array.pickle", "wb"))
pickle_output = pickle.load(open(path_trained_model + "unmodified_description_array.pickle", "rb"))
pickle_output[1]


## COMMENT THIS AND ALPHA AND CHECK BETA AND REMOVE BETA
## COMMENT PICKLE AND SCIPY BOTH USED
## COMMENT WHY rating_array and track_name_array used and all other trained model are being used
## Move rating_array code and pickle codes up



