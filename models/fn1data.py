import csv
from csv import DictReader
from os import path
import sys
import nlp_tools
import ctypes
from nlp_tools import make_embeddings_dict, save_file, load_file, remove_punc, remove_stopwords, lemmatize
import numpy as np
import errno
import os

FIELDNAMES = ['Headline', 'Body ID', 'Stance']
emb_file = 'emb_dict.pkl'
empty_array = np.array([0]*50)

def parse_text(text):
    no_punctuation = remove_punc(text)
    no_stopwords = remove_stopwords(no_punctuation)
    lemmatized = lemmatize(no_stopwords)
    return lemmatized

class fn1data():
    def __init__(self):
        print("Reading dataset")
        self.train_titles, self.train_bodies, self.train_labels, self.test_titles, self.test_bodies, self.test_labels = self.load_data()


    def load_data(self, filename=["train_stances.csv", "train_bodies.csv"], data_path=path.join(path.dirname(path.dirname(path.abspath(__file__))), 'fnc-1')):
        train_stance = self.load_dataset(filename[0], data_path)
        train_body = self.load_dataset(filename[1], data_path)

        # train_stance: a list of dicts with keys: 'Headline', 'Body ID', 'Stance'
        # train_body: a list of dicts with keys: 'Body ID', 'articleBody'

        all_title_data = []
        all_body_data = []
        all_label_data = []

        ### Parse and embed all the data ###

        id_to_headlines_stances_bodies = {}
        
        for train_dict in train_stance:
            id_article = train_dict['Body ID']
            headline_stance = [train_dict['Headline'], train_dict['Stance']]
            id_to_headlines_stances_bodies[id_article] = headline_stance

        for train_dict in train_body:
            id_to_headlines_stances_bodies[train_dict['Body ID']].append(train_dict['articleBody'])

        for train_id in id_to_headlines_stances_bodies:
            temp = id_to_headlines_stances_bodies[train_id]
            all_title_data.append(parse_text(temp[0]))
            all_label_data.append(parse_text(temp[1]))
            all_body_data.append(parse_text(temp[2]))

        all_title_embeddings, all_body_embeddings = self.word_embeddings(all_title_data, all_body_data)

        ### Separate into training data and validation data ###
        
        train_titles = np.array(all_title_embeddings[:int(len(all_title_embeddings) * 0.75)])
        test_titles = np.array(all_title_embeddings[int(len(all_title_embeddings) * 0.75):])
        train_bodies = np.array(all_body_embeddings[:int(len(all_body_embeddings) * 0.75)])
        test_bodies = np.array(all_body_embeddings[int(len(all_body_embeddings) * 0.75):])
        train_labels = np.array(all_label_data[:int(len(all_body_embeddings) * 0.75)])
        test_labels = np.array(all_label_data[int(len(all_body_embeddings) * 0.75):])

        return train_titles, train_bodies, train_labels, test_titles, test_bodies, test_labels


    def load_dataset(self, filename, data_path):
        data = None
        try:
            with open(path.join(data_path, filename), encoding='utf-8') as fh:
                reader = csv.DictReader(fh)
                data = list(reader)

                if data is None:
                    error = 'ERROR: No data found in: {}'.format(filename)
                    raise error
        except FileNotFoundError:
            error = "ERROR: Could not find file: {}".format(filename)
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)

        return data


    def word_embeddings(self, titles, bodies):
        emb_dict = load_file(emb_file)
        all_title_embeddings = []
        for title in titles:

            title_embeddings = []
            for word in title:
                # word = word.lower()
                #print(word)
                # if the word is OOV, append the unk vector
                if emb_dict.get(word) is None:
                    title_embeddings.append(emb_dict.get('unk')) # POTENTIALLY CHANGE WHAT TO APPEND
                else:
                    title_embeddings.append(emb_dict.get(word))

            if len(title_embeddings) > 13:
                title_embeddings = title_embeddings[:13]
            elif len(title_embeddings) < 13:
                while len(title_embeddings) < 13:
                    title_embeddings.append(empty_array)

            all_title_embeddings.append(title_embeddings)

        all_body_embeddings = []
        for body in bodies:
            body_embeddings = []
            for word in body:
                # if the word is OOV, append the unk vector
                if emb_dict.get(word) is None:
                    body_embeddings.append(emb_dict.get('unk')) # POTENTIALLY CHANGE WHAT TO APPEND
                else:
                    body_embeddings.append(emb_dict[word])

            if len(body_embeddings) > 500:
                body_embeddings = body_embeddings[:500]
            elif len(body_embeddings) < 500:
                while len(body_embeddings) < 500:
                    body_embeddings.append(empty_array)

            all_body_embeddings.append(body_embeddings)
        return all_title_embeddings, all_body_embeddings
