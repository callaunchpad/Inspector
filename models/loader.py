from nlp_tools import make_embeddings_dict, save_file, load_file, remove_punc, remove_stopwords, lemmatize
from dataset import Dataset
from os import path

glove_dir = "./glove.6B"
glove_50d = path.join(glove_dir, "glove.6B.50d.txt")
glove_100d = path.join(glove_dir, "glove.6B.100d.txt")
glove_200d = path.join(glove_dir, "glove.6B.200d.txt")
glove_300d = path.join(glove_dir, "glove.6B.300d.txt")

emb_file = 'emb_dict.pkl'
save_file(emb_file, make_embeddings_dict(glove_50d))
emb_dict = load_file(emb_file)
dset = Dataset()

ex = dset.bodies[0]
ex = remove_punc(ex)
ex = remove_stopwords(ex)
ex = lemmatize(ex)
print(ex)

