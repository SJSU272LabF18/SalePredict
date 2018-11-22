## Either use Stemming or use lemmatization - Lemmatization would probably be better for our use case

## Stemming - Is Stemming required? Which one? If stemming is done then for eg. Unversity is stemmed to Univers which can be confused with Universal
## Porter Stemmer
stemmer = PorterStemmer()
def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        if(item not in stop_words):
            stemmed.append(stemmer.stem(item))
    return stemmed   
    
    
## Calling Stemming function
stemmed_1 = stem_tokens(words_tokens_1, stemmer)    
