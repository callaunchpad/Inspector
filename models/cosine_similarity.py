from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import numpy as np

def cosine_sim_matrices(text_embeddings, title_embeddings):
    count_vectorizer = CountVectorizer()
    arr_text_embeddings, arr_title_embeddings = search(word)
    only_text_embeddings = []
    only_title_embeddings = []

    #get only embeddings
    for i in range(len(text_embeddings)):
        only_text_embeddings.append(arr_text_embeddings[i][0])
        only_title_embeddings.append(arr_title_embeddings[i][0])

    text_sparse_matrix = count_vectorizer.fit_transform(only_text_embeddings)
    title_sparse_matrix = count_vectorizer.fit_transform(only_title_embeddings)

    text_similarity_matrix = cosine_similarity(text_sparse_matrix)
    title_similarity_matrix = cosine_similarity(title_sparse_matrix)

    return avg(text_similarity[1:]), avg(title_similarity[1:])

def cos_sim_avgs(text_embeddings, title_embeddings):

    avg_text = np.mean(text_embeddings, axis=0)
    avg_title = np.mean(title_embeddings, axis=0)

    cos_sim = np.dot(avg_text, avg_title))
    return cos_sim


TEST_text = [np.array([1, 2, 3, 4, 5]), np.array([1, 2, 3, 4, 5]), np.array([1, 2, 3, 4, 5])]
TEST_title = [np.array([-1, -2, -3, -4, -5]), np.array([6, 7, 8, 9, 10])]

cos_sim_avgs(TEST_text, TEST_title)
