import csv
from csv import DictReader
from os import path
import sys
import nlp_tools

csv.field_size_limit(sys.maxsize)
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
                titles.append(line['title'])
                bodies.append(line['text'])
                labels.append(line['type'])
        return ids, titles, bodies, labels
    def test():
        print("hello")
# dataset = Dataset()
# print(dataset.articles[4].split(" "))