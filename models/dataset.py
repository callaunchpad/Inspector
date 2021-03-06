import csv
from csv import DictReader
from os import path
import sys
import nlp_tools
import ctypes
from nlp_tools import make_embeddings_dict, save_file, load_file, remove_punc, remove_stopwords, lemmatize

# parses the string (body or title) and returns an array of tokens
def parse_text(text):
    no_punctuation = remove_punc(text)
    no_stopwords = remove_stopwords(no_punctuation)
    lemmatized = lemmatize(no_stopwords)
    return lemmatized

csv.field_size_limit(int(ctypes.c_ulong(-1).value // 2))
# Dataset class for the CNN data
class Dataset():
    def __init__(self, filename="all_data.csv", path='../CNN_data'):
        self.data_path = path

        print("Reading dataset")

        ids, titles, bodies, labels = self.read(filename)
        self.ids = ids
        self.titles = titles
        self.bodies = bodies
        self.labels = labels

    # reads the all_csv file from the CNN_data folder and returns
    # the article ids, titles, bodies, and labels
    def read(self, filename):
        ids, titles, bodies, labels = [], [], [], []
        with open(path.join(self.data_path, filename),'r', encoding='utf-8', newline='') as csv:
            reader = DictReader(csv)
            # for row in itertools.islice(reader, 1):
            #     print("title: ", row['text'])
            for line in reader:
                ids.append(line['uuid'])
                titles.append(parse_text(line['title']))
                bodies.append(parse_text(line['text']))
                labels.append(1 if line['type'] == 'real' else 0)
        return ids, titles, bodies, labels
# dataset = Dataset()
# print(dataset.articles[4].split(" "))
