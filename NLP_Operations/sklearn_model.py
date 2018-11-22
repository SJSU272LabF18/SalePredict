from sklearn.feature_extraction.text import TfidfVectorizer

## Refer - https://machinelearningmastery.com/prepare-text-data-machine-learning-scikit-learn/
## countVectorizer - does it lowercase and remove punc and remove stopwords for whole documents with paragraphs? Stopwords?
## tfidfVectorizer - does it lowercase and remove punc and remove stopwords for whole documents with paragraphs? Stopwords?

## Either use countVectorizer and then tfidf transforms and fit, or use tfidfVectorizer

sentence_1 = "My name is Clark Kent. I am currently a Masters student at the San Jose State University. "
sentence_2 = "Clark is doing his Masters study in the Software Engineering course. Started in the year 2018"

sentence_3 = "My name is Martha Kent. I am an employee at Google, Mountain View"
sentence_4 = "Martha is currently a Programmer Analyst at Google. Started in the year 2015"

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
    vector = vectorizer.transform([sentence_array[i]])
    ## summarize encoded vector
    all_documents_encoded.append(vector.toarray())
    
## print the range of a document vector
print(vector.shape)
## print each document vector and its index   
for j in range(len(all_documents_encoded)):
    print (all_documents_encoded[j], j)
