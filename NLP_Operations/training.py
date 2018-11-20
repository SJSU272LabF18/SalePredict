import nltk
import string
#nltk.download('stopwords')
#nltk.download('punkt')
from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from collections import Counter

#Filtering the sentences
stop_words = set(stopwords.words('english'))
## stop_words stores all the stop words such as 'the', 'a', etc that would have to be removed from the dataset of description, and the description entered 
##set used so that finding and removing stop words is faster
#print (stop_words)

sentence_1 = "My name is Clark Kent and I am currently a Masters student at the San Jose State University"
sentence_2 = "Clark is doing his Masters study in the Software Engineering course. Started in the year 2018"

sentence_3 = "My name is Martha Kent and I am an employee at Google, Mountain View"
sentence_4 = "Martha is currently a Programmer Analyst at Google. Started in the year 2015"

# Replaces escape character with space 
# sentence_1a = sentence_1.replace("\n", " ") 

sentence_1 = sentence_1.lower()
sentence_2 = sentence_2.lower()
sentence_3 = sentence_3.lower()
sentence_4 = sentence_4.lower()
#Setting all words to lower case so that 'Shreyam' and 'shreyam' are counted as same

tokenizer = RegexpTokenizer(r'\w+')
#Tokenizer which also has the ability to get rid of punctualtions 

words_tokens_1 = tokenizer.tokenize(sentence_1)
filtered_sentence_1 = [w for w in words_tokens_1 if not w in stop_words]
words_tokens_2 = tokenizer.tokenize(sentence_2)
filtered_sentence_2 = [w for w in words_tokens_2 if not w in stop_words]
words_tokens_3 = tokenizer.tokenize(sentence_3)
filtered_sentence_3 = [w for w in words_tokens_3 if not w in stop_words]
words_tokens_4 = tokenizer.tokenize(sentence_4)
filtered_sentence_4 = [w for w in words_tokens_4 if not w in stop_words]

count_1 = Counter(filtered_sentence_1)
#print(count_1)
all_filtered_words_tokens = [filtered_sentence_1, filtered_sentence_2, filtered_sentence_3, filtered_sentence_4]
print (all_filtered_words_tokens)

#Gives frequency of each token in a 1D array of tokens (arranged in descending order)

#NOTE - Can words_tokens_1 become a set so then when we run find  when description is entered, it is O(1)
#NOTE - In Stopwords text file you can add words such as app, application, apple, etc that are bound to have more frequency. In this way you might not have to use tf-idf from skikit learn but would this method be slower?
#NOTE - Is Stemming required

def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)
#jaccard_similarity biased towards documents having larger length as union increases with increase in tokens
print (jaccard_similarity(filtered_sentence_1, filtered_sentence_2))

# Stemming
#Cosine and word to vector
