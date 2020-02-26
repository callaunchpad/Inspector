from os import path
import numpy as np
import pickle
from scipy import spatial
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

# nltk.download()

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stopword_set = set(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')

glove_dir = "./glove.6B"
glove_50d = path.join(glove_dir, "glove.6B.50d.txt")
glove_100d = path.join(glove_dir, "glove.6B.100d.txt")
glove_200d = path.join(glove_dir, "glove.6B.200d.txt")
glove_300d = path.join(glove_dir, "glove.6B.300d.txt")

# Creates an embedding dictionary. Each key is a word, and each value
# is a vector of size 50 for now
def make_embeddings_dict():
    embeddings_dict = {}
    with open(glove_50d, 'r') as f:
        for line in f:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = vector
    return embeddings_dict

# Creates and saves an embedding dictionary as a pickle file
# under the name filename.  
def save_file(filename, contents):
    with open(filename, 'wb') as f:
        pickle.dump(contents, f)
    
# loads a pickle file to be used as a python object
def load_file(filename):
    with open(filename, 'rb') as f:
        loaded_object = pickle.load(f)
        return loaded_object

# finds the closest word to the embedding input
def find_closest_embeddings(embedding, embeddings_dict):
    return sorted(embeddings_dict.keys(),
                  key=lambda word: spatial.distance.euclidean(embeddings_dict[word],
                  embedding))

def remove_punc(text):
    return tokenizer.tokenize(text.lower())

def remove_stopwords(text_array):
    return [w for w in text_array if w not in stopword_set]

def lemmatize(text_array):
    return [lemmatizer.lemmatize(w) for w in text_array]

def stem(text_array):
    return ' '.join([stemmer.stem(w) for w in text_array])