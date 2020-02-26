from os import path
import numpy as np
import pickle
from scipy import spatial

# import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer


lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
stopword_set = set(stopwords)
tokenizer = RegexpTokenizer(r'\w+')

glove_dir = "./glove.6B"
glove_50d = path.join(glove_dir, "glove.6B.50d.txt")
glove_100d = path.join(glove_dir, "glove.6B.100d.txt")
glove_200d = path.join(glove_dir, "glove.6B.200d.txt")
glove_300d = path.join(glove_dir, "glove.6B.300d.txt")

# Creates an embedding dictionary. Each key is a word, and each value
# is a vector of size 50 for now
# pass in one of the paths to a glove model (50d, 100d, 200d, or 300d)
def make_embeddings_dict(glove_model):
    embeddings_dict = {}
    with open(glove_model, 'r') as f:
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

# removes punctuation from a peice of text, and returns an array
def remove_punc(text):
    return tokenizer.tokenize(text.lower())

# removes stopwords from an array of strings
def remove_stopwords(text_array):
    return [w for w in text_array if w not in stopword_set]

# reduces words to a common word base. I.E consult, consultant, consulting all become consult
# stemming tends to just chop of heads and tails of words
def stem(text_array):
    return ' '.join([stemmer.stem(w) for w in text_array])

# lemmatizing is a slightly more involved way of reducing words to a common root
def lemmatize(text_array):
    return [lemmatizer.lemmatize(w) for w in text_array]