## Refer - http://billchambers.me/tutorials/2014/12/21/tf-idf-explained-in-python.html
def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)
## jaccard_similarity biased towards documents having larger length as union increases with increase in tokens
## Can we make document lengths same by converting them to vectors and then apply this similarity?
#print (jaccard_similarity(,))
