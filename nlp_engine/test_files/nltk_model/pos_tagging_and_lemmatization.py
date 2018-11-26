import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
lemmatizer = WordNetLemmatizer()

## Either use Stemming or use lemmatization - Lemmatization would probably be better for our use case

## Refer - https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
## Refer - https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
## Refer - https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk
## Refer - https://www2.cs.duke.edu/courses/spring14/compsci290/assignments/lab02.html


tokens1 = ['My', 'name', 'is', 'Clark', 'Kent', 'and', 'i', 'am', 'A', 'student', 'at', 'the', '-', 'SAN', 'jose', 'state', 'university']
tokens2 = ['my', 'name', 'is', 'clark', 'kent', 'and', 'i', 'am', 'a', 'student', 'at', 'the', 'SAN', 'jose', 'state', 'university']

tokens3 = ['name', 'Clark', 'Kent', 'student', '-',  'san', 'jose', 'state', 'university']
tokens4 = ['name', 'clark', 'kent', 'student', 'San', 'jose', 'state', 'university']

## POS tagging & Lemmatization - But with or without the stopwords and punctuation? - Does lemmatization require 'a', 'the', etc and such context around words to run properly?

'''
 Method -
 Input sentence. Tokenize/Remove punctuation. Stop words remove. POS Tag. 
 Captitalization of the word affects POS tagging. Does punctuation also affect?
 Then Lemmatize. Then Lowercase.
 NOTE - We can improve performance by making our own tokenizing function and in that we split every word on space and pos tag it and lemmatize the word. So we save complexity as by using inbuilt func we are running over the list twice as once when tokenizing and once while lemmatizing
'''

tag_1 = nltk.pos_tag(tokens1)
print (tag_1)
tag_2 = nltk.pos_tag(tokens2)
print (tag_2)
tag_3 = nltk.pos_tag(tokens3)
print (tag_3)
tag_4 = nltk.pos_tag(tokens4)
print (tag_4)


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

def lemmatize_tokens(tokens_with_tag):
    for i in range(len(tokens_with_tag)):
        print (lemmatizer.lemmatize(tokens_with_tag[i][0],get_wordnet_pos(tokens_with_tag[i][1])))


lemmatize_tokens(tag_1)
lemmatize_tokens(tag_2)
lemmatize_tokens(tag_3)
lemmatize_tokens(tag_4)
