from os import path
import numpy as np
import pickle
from scipy import spatial
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
nltk.data.path.append('./nltk_data')
# nltk.download()

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
stopword_set = set(stopwords.words('english'))
tokenizer = RegexpTokenizer(r'\w+')

# Creates an embedding dictionary. Each key is a word, and each value
# is a vector of size 50 for now
def make_embeddings_dict(glove_path):
    embeddings_dict = {}
    with open(glove_path, 'r', encoding='utf8') as f:
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