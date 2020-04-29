import bs4
from bs4 import BeautifulSoup as soup
import numpy as np
from urllib.request import urlopen
from nlp_tools import make_embeddings_dict, save_file, load_file, remove_punc, remove_stopwords, lemmatize
emb_file = 'emb_dict.pkl'

def search(word):
    news_url = "http://news.google.com/news?q={0}&hl=en&prmd=imvns&um=1&ie=UTF-8&output=rss".format(word)

    Client = urlopen(news_url)
    xml_page = Client.read()
    Client.close()
    soup_page = soup(xml_page,"xml")
    news_list = soup_page.findAll("item")

    arr_text_embeddings = [] #list of tuple(text_embeddings, article_link)
    arr_title_embeddings = []
    for i in range(4):
        text_embedding_tuple = get_text_embeddings(i)
        arr_text_embeddings.append(text_embedding_tuple)

        title_embedding_tuple = get_title_embeddings(i)
        arr_title_embeddings.append(title_embedding_tuple)

    return (arr_text_embeddings, arr_title_embeddings) 

def get_text_embeddings(index):
    article = news_list[index]
    article_link = article.link.text

    Article_Client = urlopen(article_link)
    art_xml_page = Article_Client.read()
    Article_Client.close()
    art_soup_page = soup(xml_page, "xml")
    article_text = soup.find('p').getText()

    article_text_parsed = parse_text(article_text)
    article_text_embeddings = word_embeddings(article_text_parsed)

    return (article_text_embeddings, article_link)

def get_title_embeddings(index):
    article = news_list[index]
    article_link = article.link.text

    Article_Client = urlopen(article_link)
    art_xml_page = Article_Client.read()
    Article_Client.close()
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title')
    title_embeddings = word_embeddings(title)

    return (title_embeddings, article_link)

def parse_text(text):
    no_punctuation = remove_punc(text)
    no_stopwords = remove_stopwords(no_punctuation)
    lemmatized = lemmatize(no_stopwords)
    return lemmatized

def word_embeddings(text):
        emb_dict = load_file(emb_file)
        embeddings = []
        for word in text:
            # word = word.lower()
            #print(word)
            # if the word is OOV, append the unk vector
            if emb_dict.get(word) is None:
                embeddings.append(emb_dict.get('unk')) # POTENTIALLY CHANGE WHAT TO APPEND
            else:
                embeddings.append(emb_dict.get(word))

        embeddings = np.asarray(embeddings)
        return embeddings

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

def cosine_sim_matrices(text_embeddings, title_embeddings):
    count_vectorizer = CountVectorizer()
    arr_text_embeddings, arr_title_embeddings = search(word)
    only_text_embeddings = []
    only_title_embeddings = []

    #get only embeddings
    for i in range(4):
        only_text_embeddings.append(arr_text_embeddings[i][0])
        only_title_embeddings.append(arr_title_embeddings[i][0])

    text_sparse_matrix = count_vectorizer.fit_transform(only_text_embeddings)
    title_sparse_matrix = count_vectorizer.fit_transform(only_title_embeddings)

    text_similarity_matrix = cosine_similarity(text_sparse_matrix)
    title_similarity_matrix = cosine_similarity(title_sparse_matrix)

    return avg(text_similarity[1:]), avg(title_similarity[1:])

def cos_sim_avgs(text_embeddings, title_embeddings):
    return None
    
print(search("corona"))
