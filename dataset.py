from csv import DictReader
from os import path
class Dataset():
    def __init__(self, name="train", path='./fnc-1'):
        self.path = path

        print("Reading dataset")
        bodies = name+"_bodies.csv"
        stances = name+"_stances.csv"

        self.stances = self.read(stances)
        articles = self.read(bodies)
        self.articles = dict()

        #make the body ID an integer value
        for s in self.stances:
            s['Body ID'] = int(s['Body ID'])

        #copy all bodies into a dictionary
        for article in articles:
            self.articles[int(article['Body ID'])] = article['articleBody']

        print("Total stances read: " + str(len(self.stances)))
        print("Total bodies read: " + str(len(self.articles)))


    def read(self, filename):
        rows = []
        with open(path.join(self.path, filename),'r', encoding='utf-8') as table:
            r = DictReader(table)
            for line in r:
                rows.append(line)
        return rows

dataset = Dataset()
print(dataset.articles[4].split(" "))