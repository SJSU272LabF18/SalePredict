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

## if df>>tf then is tfidf very very near 0 such that it wont show even with a double datatype? For this do we multiply tf by a constant to make it comparable to idf and make tfidf calculatable with avaiable datasets?

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
    
## NOTE - There are 2 approaches for creating or prediction model
## 1st (could be more accurate) - Our model is a x-y plot in which each point represents a sparse array on x and the rating associated on y. Is it possible to assign a unique number to each sparse array? THis number would be on x and the associated rating would be on y. Then when form the whole graph and when a new sparse array (from new description) is entered then we match its y from the graph
## 2nd - Our model finds k szimilar sparse arrays to our new sparse array. The ratings associated with theses k similar arrays are weighted averaged which gives us the prediced rating
### In 2nd approach the innate idea is that we assume that the average rating of the apps matching the new description can probably be the potential rating. But in real life many other constraints act such as is the app free or is it paid, where is the app being release, etc and these constraints drive the app rating, which is not handled by this approach. It could be possible that the new description is very similar to a particular set of apps but when actually deployed, it gets very low ratings than actual due to some unforeseen reasons. This is somewhat handled by using weighted average. But then we should also keep in mind that ML is statistics only, and real world constraints and ambiguity cannot all be accounted for. Keep in mind that ML basically tells us how y should be for a new x in ideal conditions. But due to real world constraints, ideal case is not experienced generally. One thing we can do to take into the real world constraints is that when the averaging model is complete then we add improvements such as taking into account if the apps are paid or not, demographics of the app, technologies used and so on. 
### The 1st approach is a regression approach which actually makes a plot of description on x and its corresponding rating on y. It could be possible that this plot accounts for all these different real world constraints, as it is essentialy making a plot of real world trend of how the apps do. But this is only a speculation, we're not sure exactly if the method would be able to predict a new description rating with decent accuracy or not. This method involves plotting the sparse arrays on the x axex different points. How do we do this? One method could be to take [0, 0, 0, ..] as origin and [1, 1, 1, ...] as the max x value. Now each sparse array is at a distance from the origin. But if we only take into account the euclidean distance then 2 different descriptions can have same distance from origin as when their arrays are plotted in x-y plane, they are at different angles from the origin but are at the same distance. So we can multiply the distance with the cosine angle to form unique real number value for each description that can be then plotted on the x axis in out regression plot, with rating on the y axis. But does this method might have some misconceptions that we cannot think of right now. 
### Therefore we move forward with the second approach.

## 2nd approach- Find Similarity: 
## Do cosine similarity and euclidean distance have the same effect? Jaccard similarity? KNN?
## Run all above functions on a new input
## Find Weighted Average of Ratings

'''
## Test Sentence 

## vectorizer.<some_function> to remove the new words that are not in the vocab
## Or make vocab as a set and then check for each word in the new description. If present in set then push it into array which will be transformed
vectorNew = vectorizer.transform(test_sentence)

print(vectorNew)
'''
