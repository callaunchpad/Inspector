from nlp_tools import save_file, load_file
from dataset import Dataset
from os import path
import numpy as np

empty_array = np.array([0]*50)

emb_file = 'emb_dict.pkl'
dset_file = 'dataset_obj.pkl'

def load_data():
    emb_dict = load_file(emb_file)
    dset = load_file(dset_file)
    all_title_embeddings = []
    for title in dset.titles:

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
    for body in dset.bodies:
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

    train_title = np.array(all_title_embeddings[:int(len(all_title_embeddings) * 0.75)])
    test_title = np.array(all_title_embeddings[int(len(all_title_embeddings) * 0.75):])
    train_body = np.array(all_body_embeddings[:int(len(all_body_embeddings) * 0.75)])
    test_body = np.array(all_body_embeddings[int(len(all_body_embeddings) * 0.75):])
    train_labels = np.array(dset.labels[:int(len(all_body_embeddings) * 0.75)])
    test_labels = np.array(dset.labels[int(len(all_body_embeddings) * 0.75):])

    return train_title, test_title, train_labels, train_body, test_body, test_labels
