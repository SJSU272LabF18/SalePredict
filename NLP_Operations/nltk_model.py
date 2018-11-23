import nltk
import string
#nltk.download('stopwords')
#nltk.download('punkt') 
#nltk.download('averaged_perceptron_tagger') ## Used for POS tagging
#nltk.download('wordnet') ## Dictionary
from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
#from nltk.stem.porter import *
from collections import Counter

## Refer - https://www.youtube.com/watch?v=05ONoGfmKvA
## Refer - https://www2.cs.duke.edu/courses/spring14/compsci290/assignments/lab02.html
## Refer - https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk
## Refer - https://www.oreilly.com/learning/how-do-i-compare-document-similarity-using-python

''' NOTE - # is Commented Code and ## is just Comment'''
## stop_words stores all the stop words such as 'the', 'a', etc that would have to be removed from the dataset of description, and the description entered 
stop_words = set(stopwords.words('english'))
## set used so that finding and removing stop words is faster
#print (stop_words)
## NOTE - In Stopwords text file we can add words such as app, application, apple, etc that are bound to have more frequency. In this way we might not have to use tf-idf from skikit learn but would this method be slower?

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

## Initially we do not apply further preprocessing steps such as Stemming or Lemmatization and so on. First we train a basic model and then we can apply these advanced methods of text mining to increase accuracy. But would these modifications actually increase accuracy?

## Extracting and storing tokens from a token array while not storing stop words
words_tokens_1 = tokenizer.tokenize(sentence_1)
## Can increase performance by making our own regex tokenizer so that takenizing and and removing stop words takes place in the same iteration
filtered_sentence_1 = [w for w in words_tokens_1 if not w in stop_words]
words_tokens_2 = tokenizer.tokenize(sentence_2)
filtered_sentence_2 = [w for w in words_tokens_2 if not w in stop_words]
words_tokens_3 = tokenizer.tokenize(sentence_3)
filtered_sentence_3 = [w for w in words_tokens_3 if not w in stop_words]
words_tokens_4 = tokenizer.tokenize(sentence_4)
filtered_sentence_4 = [w for w in words_tokens_4 if not w in stop_words]

## NOTE - Can words_tokens_1 become a set so then when we run find when description is entered, it is O(1)

count_1 = Counter(filtered_sentence_1)
print(count_1)
## Gives frequency of each token in a 1D array of tokens (arranged in descending order)

all_words_tokens = [filtered_sentence_1, filtered_sentence_2, filtered_sentence_3, filtered_sentence_4]
print (all_words_tokens)

## tf-idf? To make document length same?
## Cosine Similarity, euclidean distance, word/document to vector

## Run all above functions on a new input
## Naive Bayes
## Weighted Average
## Find Similarity 
