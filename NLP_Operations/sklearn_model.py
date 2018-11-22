from sklearn.feature_extraction.text import TfidfVectorizer

''' NOTE - # is Commented Code and ## is just Comment'''

## Refer - https://machinelearningmastery.com/prepare-text-data-machine-learning-scikit-learn/
## countVectorizer - does it lowercase and remove punc and remove stopwords for whole documents with paragraphs? Stopwords?
## tfidfVectorizer - does it lowercase and remove punc and remove stopwords for whole documents with paragraphs? Stopwords?

## Either use countVectorizer and then tfidf transforms and fit, or use tfidfVectorizer

sentence_1 = "My name is Clark Kent. I am currently a Masters student at the San Jose State University. "
sentence_2 = "Clark is doing his Masters study in the Software Engineering course. Started in the year 2018"

sentence_3 = "My name is Martha Kent. I am an employee at Google, Mountain View"
sentence_4 = "Martha is currently a Programmer Analyst at Google. Started in the year 2015"

test_sentence = "The quick brown fox jumps over the lazy dog"

sentence_array = [sentence_1,sentence_2,sentence_3,sentence_4]

## the indexes of the whole document array (sentence_array) could work as the unique id (primary key) of each description from the dataset
## if a description is NaN then store some indicator or '' here and move to next index

## create the transform
vectorizer = TfidfVectorizer(stop_words = 'english')
## NOTE - does removing stop_words = 'english' above decrease accuracy of model?
## Edited the stop_words.py file. Would have to download the original stop_words.py if required in other projects

## tokenize and build vocabulary
vectorizer.fit(sentence_array)

## summarize
print(vectorizer.vocabulary_)
print(vectorizer.idf_)

## encode each document and save in a combined array
all_documents_encoded = []
for i in range(len(sentence_array)):
    vector = vectorizer.transform([sentence_array[i]]) ## make sparse array
    ## summarize encoded vector
    all_documents_encoded.append(vector.toarray())
    
    
    
## print the range of a document vector
print(vector.shape)
## print each document vector and its index   
for j in range(len(all_documents_encoded)):
    print (all_documents_encoded[j], j)
    
'''
## Test Sentence 

## vectorizer.<some_function> to remove the new words that are not in the vocab
## Or make vocab as a set and then check for each word in the new description. If present in set then push it into array which will be transformed
vectorNew = vectorizer.transform(test_sentence)

print(vectorNew)
'''

## Find Similarity: 
## Do cosine similarity and euclidean distance have the same effect? Jaccard similarity? KNN?
## Run all above functions on a new input
## Naive Bayes?

## Weighted Average

## NOTE - There are 2 approaches for creating or prediction model
## 1st (Probably more accurate) - Our model is a x-y plot in which each point represents a sparse array on x and the rating associated on y. Is it possible to assign a unique number to each sparse array? THis number would be on x and the associated rating would be on y. Then when form the whole graph and when a new sparse array (from new description) is entered then we match its y from the graph
## 2nd - Our model finds k similar sparse arrays to our new sparse array. The ratings associated with theses k similar arrays are weighted averaged which gives us the prediced rating
