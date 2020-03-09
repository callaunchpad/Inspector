import csv
from csv import DictReader
from os import path
import sys
import nlp_tools
import ctypes
from nlp_tools import make_embeddings_dict, save_file, load_file, remove_punc, remove_stopwords, lemmatize

FIELDNAMES = ['Headline', 'Body ID', 'Stance']

def parse_text(text):
    no_punctuation = remove_punc(text)
    no_stopwords = remove_stopwords(no_punctuation)
    lemmatized = lemmatize(no_stopwords)
    return lemmatized

class fn1data():
    def __init__(self):
        print("Reading dataset")
        self.train_titles, self.train_bodies, self.train_labels, self.test_titles, self.test_bodies, self.test_labels = load_data()


    def load_data(filename=["train_stances.csv", "train_bodies.csv", "test_bodies.csv", "test_stances_unlabeled.csv"], path='../fnc-1'):
        train_stance = load_dataset(filename[0]) #train_stance
        test_stance = load_dataset(filename[3]) #test_stance
        train_body = load_dataset(filename[1]) #train_bodies
        test_body = load_dataset(filename[2]) #test_bodies

        train_titles = []
        train_bodies = []
        train_labels = []
        test_titles = []
        test_bodies = []
        test_labels = []

        id_to_stance_headlines = {}
        for dict in train_stance:
            id = dict['Body ID']
            stance_headline = [dict['Headline'], dict['Stance']]
            id_to_stance_headlines[id] = stance_headline

        for dict in train_body:
            id_to_stance_headlines[dict['Body ID']].append(dict['articleBody'])

        for id in id_to_stance_headlines:
            temp = id_to_stance_headlines[id]
            train_titles.append(parse_text(temp[0]))
            train_labels.append(parse_text(temp[1]))
            train_bodies.append(parse_text(temp[2]))

        id_to_stance_headlines_test = {}
        for dict in test_stance:
            id = dict['Body ID']
            stance_headline_test = [dict['Headline'], dict['Stance']]
            id_to_stance_headlines_test[id] = stance_headline_test

        for dict in test_body:
            id_to_stance_headlines_test[dict['Body ID']].append(dict['articleBody'])

        for id in id_to_stance_headlines_test:
            temp = id_to_stance_headlines_test[id]
            test_titles.append(parse_text(temp[0]))
            test_labels.append(parse_text(temp[1]))
            test_bodies.append(parse_text(temp[2]))

        train_titles, train_bodies = word_embeddings(train_titles, train_bodies)
        test_titles, test_bodies = word_embeddings(test_titles, test_bodies)

        return train_titles, train_bodies, train_labels, test_titles, test_bodies, test_labels


    def load_dataset(filename):
        data = None
        try:
            with open(path.join(self.data_path, filename)) as fh:
                reader = csv.DictReader(fh)
                data = list(reader)

                if data is None:
                    error = 'ERROR: No data found in: {}'.format(filename)
                    raise FNCException(error)
        except FileNotFoundError:
            error = "ERROR: Could not find file: {}".format(filename)
            raise FNCException(error)

        return data


    def word_embeddings(titles, bodies):
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
