import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
lemmatizer = WordNetLemmatizer()


tokens1 = ['My', 'name', 'is', 'Shreyam', 'Kela', 'and', 'i', 'am', 'A', 'student', 'at', 'the', '-', 'SAN', 'jose', 'state', 'university']
tokens2 = ['my', 'name', 'is', 'shreyam', 'kela', 'and', 'i', 'am', 'a', 'student', 'at', 'the', 'SAN', 'jose', 'state', 'university']

tokens3 = ['name', 'Shreyam', 'Kela', 'student', '-',  'san', 'jose', 'state', 'university']
tokens4 = ['name', 'shreyam', 'kela', 'student', 'San', 'jose', 'state', 'university']

# Input sentence. Tokenize/Remove punctuation. Stop words remove. POS Tag. 
# Captitalization of the word affects POS tagging. Does punctuation also affect?
# Then Lemmatize. Then Lowercase.
# NOTE - We can improve performance by making our own tokenizing function and in that we split every word on space and pos tag it and lemmatize the word. So we save complexity as by using inbuilt func we are running over the list twice as once when tokenizing and once while lemmatizing

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
