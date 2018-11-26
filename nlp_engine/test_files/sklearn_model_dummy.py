from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction import text
#import numpy as np
import pandas as pd ## Read and manipulate csv

''' NOTE - # is Commented Code and ## is just Comment and ### is Sub-Comment for the nearest ## above'''

## Refer - https://machinelearningmastery.com/prepare-text-data-machine-learning-scikit-learn/
## countVectorizer - does it lowercase and remove punc and remove stopwords for whole documents with paragraphs? Stopwords?
## tfidfVectorizer - does it lowercase and remove punc and remove stopwords for whole documents with paragraphs? Stopwords?

## Either use countVectorizer and then tfidf transforms and fit, or use tfidfVectorizer

description_1 = "My name is Clark Kent. I am currently a Masters student at the San Jose State University. "
description_2 = "Clark is doing his Masters study in the Software Engineering course. Started in the year 2018"

description_3 = "My name is Martha Kent. I am an employee at Google, Mountain View"
description_4 = "Martha is currently a Programmer Analyst at Google. Started in the year 2015"

test_description = "The quick brown fox Clark jumps over the lazy dog Martha. Carpe diem!"

description_array = [description_1,description_2,description_3,description_4]

## the indexes of the whole document array (description_array) could work as the unique id (primary key) of each description from the dataset
## if a description is NaN then store some indicator or '' here and move to next index

## NOTE - Stemming or Lemmatization?

## create the transform
vectorizer = TfidfVectorizer(stop_words = 'english')
## NOTE - does removing stop_words = 'english' above decrease accuracy of model?
## Edited the stop_words.py file. Would have to download the original stop_words.py if required in other projects

## if df>>tf then is tfidf very very near 0 such that it wont show even with a double datatype? For this do we multiply tf by a constant to make it comparable to idf and make tfidf calculatable for avaiable datasets?

## tokenize and build vocabulary
vectorizer.fit(description_array)

## summarize
print(vectorizer.vocabulary_)
print(vectorizer.idf_)

## encode each document and save in a combined array
all_documents_encoded = []
for i in range(len(description_array)):
    vector = vectorizer.transform([description_array[i]]) ## make sparse array
    ## summarize encoded vector
    all_documents_encoded.append(vector.toarray())
    
## print the range of a document vector
print(vector.shape)
## print each document vector and its index   
for j in range(len(all_documents_encoded)):
    print (all_documents_encoded[j], j)
    
## Handling unseen words, stop words, punctuations, and next lines in the test description and form the sparse array of test description
## is there a function in sklearn to handle new and unseen words in the testing descriptions?
tokenizer = vectorizer.build_tokenizer()
test_description_tokens = tokenizer(test_description)
print (test_description_tokens)    

## Store all words from sklearn stop words file
stop_words = text.ENGLISH_STOP_WORDS

test_description_tokens_filtered = []
for i in range(len(test_description_tokens)):
    ## if the current token lowercased is not in stop words and is present in vocabulary, then append the token to a token array
    ## vectorizer.vocabulary_ is a map therefore get() is O(1). get() returns index of that word if found in vocab. If not found it returns None
    if not test_description_tokens[i].lower() in stop_words and vectorizer.vocabulary_.get(test_description_tokens[i].lower()) != None :
        test_description_tokens_filtered.append(test_description_tokens[i].lower())

print (test_description_tokens_filtered)

## vectorizer.transform takes in string to form a sparse array of it
## Therefore, we convert tbe te description token array to string

test_description_modified = " ".join(test_description_tokens_filtered)
## "".join(['a','b','c']) means Join all elements of the array, separated by the string "". In the same way, " hi ".join(["jim", "bob", "joe"]) will create "jim hi bob hi joe"

## make sparse array of filtered test description
test_document_vector = vectorizer.transform([test_description_modified])
test_document_encoded = (test_document_vector.toarray()) 

print (test_document_encoded)

## NOTE - There are 2 approaches for creating our prediction model
## 1st (could be more accurate) - Our model is a x-y plot in which each point represents a sparse array on x and the rating associated on y. Is it possible to assign a unique number to each sparse array? THis number would be on x and the associated rating would be on y. Then when form the whole graph and when a new sparse array (from new description) is entered then we match its y from the graph
## 2nd - Our model finds k szimilar sparse arrays to our new sparse array. The ratings associated with theses k similar arrays are weighted averaged which gives us the prediced rating
### In 2nd approach the innate idea is that we assume that the average rating of the apps matching the new description can probably be the potential rating, apps with similar description are assumed to have similar ratings. Ideally also, this should be true. But in real life many other constraints act such as is the app free or is it paid, where is the app being release, etc and these constraints drive the app rating, which is not handled by this approach. It could be possible that the new description is very similar to a particular set of apps but when actually deployed, it gets very low ratings than actual due to some unforeseen reasons. This is somewhat handled by using weighted average. But then we should also keep in mind that ML is statistics only, and real world constraints and ambiguity cannot all be accounted for. Keep in mind that ML basically tells us how y should be for a new x in ideal conditions. But due to real world constraints, ideal case is not experienced generally. One thing we can do to take into the real world constraints is that when the averaging model is complete then we add improvements such as taking into account if the apps are paid or not, demographics of the app, technologies used and so on. 
### The 1st approach is a regression approach which actually makes a plot of description on x and its corresponding rating on y. It could be possible that this plot accounts for all these different real world constraints, as it is essentialy making a plot of real world trend of how the apps do. But this is only a speculation, we're not sure exactly if the method would be able to predict a new description rating with decent accuracy or not. This method involves plotting the sparse arrays on the x axex different points. How do we do this? One method could be to take [0, 0, 0, ..] as origin and [1, 1, 1, ...] as the max x value. Now each sparse array is at a distance from the origin. But if we only take into account the euclidean distance then 2 different descriptions can have same distance from origin as when their arrays are plotted in x-y plane, they are at different angles from the origin but are at the same distance. So we can multiply the distance with the cosine angle to form unique real number value for each description that can be then plotted on the x axis in out regression plot, with rating on the y axis. But does this method might have some misconceptions that we cannot think of right now. 
### Therefore we move forward with the second approach.

## 2nd approach- Find Similarity: 
## Approaches to finding similarity - 1) Cosine similarity and euclidean distance have the same effect, probably? 2) Jaccard similarity 3) KNN 4) K means clustering
### Refer - https://towardsdatascience.com/overview-of-text-similarity-metrics-3397c4601f50
### Jaccard similarity takes only unique set of words for each document. This means that if we repeat the word “friend” in a description several times, cosine similarity changes for each new "friend" word added to the description but Jaccard similarity does not change.
### Therefore we use Cosine Similarity


## Cosine Similarity:

## The usual creation of arrays produces wrong format (as cosine_similarity works on matrices)
## Therefore, if need to reshape these to numpy array
## Import numpy then:
#doc1 = doc1.reshape(1,-1)
#doc2 = doc2.reshape(1,-1)
## When shape = (n, m) it means n = number of rows and m = number of columns

all_documents_similarity = []
## all_documents_similarity is a array in whcih we save the similarity and the primary key/index together as we will have to sort the list for selecting top similar descriptions, so we need to save the indexes as well
for i in range(len(all_documents_encoded)):
    all_documents_similarity.append([cosine_similarity(all_documents_encoded[i],test_document_encoded), i])

## Sort all similarities in desc order    
all_documents_similarity_sorted = sorted(all_documents_similarity, reverse = True) 


## Select similar documents:

## Select Top X% of the sorted values
## NOTE - Is there a better way to decide what percentage to select, other than trial and error on percentages?
X = 50
topXpercent = int(len(all_documents_similarity_sorted)*(X/100))
all_documents_similarity_sorted_topXpercent = all_documents_similarity_sorted[:topXpercent]
print (all_documents_similarity)
print (all_documents_similarity_sorted)
print (topXpercent)
print (all_documents_similarity_sorted_topXpercent)

## Find Weighted Average of Ratings
## Pickle
## Server
