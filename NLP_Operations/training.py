import nltk
import string
#nltk.download('stopwords')
#nltk.download('punkt') 
#nltk.download('averaged_perceptron_tagger') ## Used for POS tagging
#nltk.download('wordnet') ## Dictionary
from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import *
from collections import Counter

''' NOTE - # is Commented Code and ## is just Comment'''
## stop_words stores all the stop words such as 'the', 'a', etc that would have to be removed from the dataset of description, and the description entered 
stop_words = set(stopwords.words('english'))
## set used so that finding and removing stop words is faster
#print (stop_words)

sentence_1 = "My name is Clark Kent and I am currently a Masters student at the San Jose State University"
sentence_2 = "Clark is doing his Masters study in the Software Engineering course. Started in the year 2018"

sentence_3 = "My name is Martha Kent and I am an employee at Google, Mountain View"
sentence_4 = "Martha is currently a Programmer Analyst at Google. Started in the year 2015"

## To replace escape character in between paragraphs with space: 
# sentence_1a = sentence_1.replace("\n", " ") 

## Setting all words to lower case so that 'Shreyam' and 'shreyam' are counted as same
sentence_1 = sentence_1.lower()
sentence_2 = sentence_2.lower()
sentence_3 = sentence_3.lower()
sentence_4 = sentence_4.lower()

## Tokenizer which also has the ability to get rid of punctualtions 
tokenizer = RegexpTokenizer(r'\w+')


'''
## Stemming - Is Stemming required? Which one? If stemming is done then for eg. Unversity is stemmed to Univers which can be confused with Universal
## Porter Stemmer
stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        if(item not in stop_words):
            stemmed.append(stemmer.stem(item))
    return stemmed    
'''


## POS tagging & Lemmatization - But with or without the stopwords and punctuation? - Does lemmatization require 'a', 'the', etc and such context to run properly?




## Either use Stemming or use lemmatization


words_tokens_1 = tokenizer.tokenize(sentence_1)
## Extracting and storing tokens from a token array while not storing stop words
#filtered_sentence_1 = [w for w in words_tokens_1 if not w in stop_words]
## Calling Stemming function
#stemmed_1 = stem_tokens(words_tokens_1, stemmer)

words_tokens_2 = tokenizer.tokenize(sentence_2)


words_tokens_3 = tokenizer.tokenize(sentence_3)


words_tokens_4 = tokenizer.tokenize(sentence_4)


count_1 = Counter(stemmed_1)
print(count_1)
## Gives frequency of each token in a 1D array of tokens (arranged in descending order)

all_stemmed_words_tokens = [stemmed_1, stemmed_2, stemmed_3, stemmed_4]
print (all_stemmed_words_tokens)


## NOTE - Can words_tokens_1 become a set so then when we run find  when description is entered, it is O(1)
## NOTE - In Stopwords text file you can add words such as app, application, apple, etc that are bound to have more frequency. In this way you might not have to use tf-idf from skikit learn but would this method be slower?

def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)
#jaccard_similarity biased towards documents having larger length as union increases with increase in tokens
#print (jaccard_similarity())

# tf-idf?
# Cosine and word to vector

# Run all above functions on a new input
# Weighted Average
# Find Similarity
