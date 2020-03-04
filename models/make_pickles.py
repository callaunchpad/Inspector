from dataset import Dataset
from os import path
from nlp_tools import save_file, load_file, make_embeddings_dict

THIS_FOLDER = path.dirname(path.abspath(__file__))

glove_dir = path.join(THIS_FOLDER, 'glove.6B')

glove_50d = path.join(glove_dir, 'glove.6B.50d.txt')
glove_100d = path.join(glove_dir, 'glove.6B.100d.txt')
glove_200d = path.join(glove_dir, 'glove.6B.200d.txt')
glove_300d = path.join(glove_dir, 'glove.6B.300d.txt')

emb_file = 'emb_dict.pkl'
dset_file = 'dataset_obj.pkl'

print("making word embedding dictionary pkl...")
save_file(emb_file, make_embeddings_dict(glove_50d))
print("making datset object pkl")
dset = Dataset(filename='all_data.csv', path=path.join(path.dirname(path.dirname(path.abspath(__file__))), 'CNN_data'))
save_file("dataset_obj.pkl", dset)