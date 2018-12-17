This folder contains all the various algorithms and code snippets that were tried/tested and discarded/used during the model building procedure.

- *nltk_model* folder: Contains code snippets related to using NLTK library for the Tokenization and Stemming/Lemmatization of the descriptions. In the final model code, both scikit-learn and NLTK libraries is used. The TfidfVectorizer function is from scikit-learn and the POS tagger and Lemmatizer is from NLTK.
- *similarity_methods* folder: Contains the code snippet for Jaccard similarity. For our application, Cosine Similarity suited better as Jaccard Similarity is biased towards longer documents (Denominator in Jaccard Similarity changes with the length of the document. Numerator may or may not change)
- *flask_server_-_dummy.py* file: Code snippet for a dummy flask server
- *include_features_from_google_to_apple_dataset.py* file: Code snippet to include features from other datasets into our dataset to form a hybrid dataset
- *sklearn_model_dummy.py* file: Code snippet for scikit learn model prediction for 4 dummy sentences. This is the primary file where model basics were developed. Finds similarity between dummy sentences.
- *sparse_matrix_to_scipyCSCmatrix_npz.py* file: Code snippet for converting a sparse matrix to npz file for storage.
- *test_-_similarity_with_manual_topX_sort.py* file: Pre-final model code that tested on dummy descriptions (using sorting of top X similar documents only)
- *test_-_similarity_with_manual_topX_sort_(FrontEnd_Display).py* file: Pre-final model code that tested on dummy descriptions and prints output to be shown on frontend
- *test_-_similarity_with_sorted_function.py* file: Pre-final model code that tested on dummy descriptions (using in-built sorting function in Python). This method is discarded.
- *translate_non_-_english_descriptions.py* file: Code snippet to translate non-english descriptions. This feature is not included into the final model. Therefore, user interface cannot take non-english descriptions.
