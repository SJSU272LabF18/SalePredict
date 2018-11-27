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


## TO BE DONE AS SOON AS SERVER STARTS RUNNING i.e description_array file should be kept open and running even when nobody is pinging on enter description
## Load full description array
description_array = pickle.load(open("description_array.pickle", "rb"))
## create the transform
vectorizer = TfidfVectorizer(stop_words = 'english')   
## tokenize and build vocabulary
vectorizer.fit(description_array)
## Load all rating array
rating_array = pickle.load(open("rating_array.pickle", "rb"))
#print (rating_array[0])
## Load all track name array
track_name_array = pickle.load(open("track_name_array.pickle", "rb"))
#print (track_name_array[0])

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


test_description = "5 previous escape games plus 1 new game in one package!  The Cupcake Shop  is the 11th escape game produced by FUNKYLAND. This special package includes the new game,  Cupcake Shop  and 5 previous escape games (Cake CafÃ©, Ice Cream Parlor, Fruit Juice Parlor, Halloween Candy Shop, and Crepe House). You can choose to play your favorite of 6 charming and easy escape games. Find the items and solve the mysteries to escape from each shop. How to Play: - Just tap - Tap the item icon twice to enlarge the display. - Tap the [+] button in the upper right hand corner to display the settings screen. Game Features: - Beautiful graphics - Auto-save - Easy and fun, even for those not keen on escape games - Perfect game length to kill time The Save Function: The game auto-saves items you've acquired and instruments you've unlocked, allowing you to restart at the last auto-save checkpoint. In case you can't restart, please check your device settings as there may not be enough storage space. The list of shops: Cupcake Shop << New!! Cake CafÃ© Ice Cream Parlor Fruit Juice Parlor Halloween Candy Shop Crepe House"
if detect(test_description) != 'en':
    print("Please enter the description in plain english.")
else:
    ## POS Tagging and Lemmatization
    lemmatized_Description = lemmatizeDescription(test_description)
    
test_description_modified = lemmatized_Description



'''
## Test Description - Tokenization and Filteration with sklearn - Without POS tagging & Lemmatization: 
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



print (test_description_modified)

## make sparse array of filtered test description
test_document_vector = vectorizer.transform([test_description_modified])
test_document_encoded = (test_document_vector.toarray()) 

#print (test_document_encoded)

## Load All Documents Encoded Sparse Array npz file
sparse_matrix = scipy.sparse.load_npz('sparse_matrix_actual.npz')
all_documents_encoded = sparse_matrix.todense()

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
print (final_rating)
