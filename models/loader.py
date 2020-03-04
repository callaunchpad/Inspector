from nlp_tools import make_embeddings_dict, save_file, load_file, remove_punc, remove_stopwords, lemmatize
from dataset import Dataset
from os import path

THIS_FOLDER = path.dirname(path.abspath(__file__))

glove_dir = path.join(THIS_FOLDER, 'glove.6B')

glove_50d = path.join(glove_dir, 'glove.6B.50d.txt')
glove_100d = path.join(glove_dir, 'glove.6B.100d.txt')
glove_200d = path.join(glove_dir, 'glove.6B.200d.txt')
glove_300d = path.join(glove_dir, 'glove.6B.300d.txt')

emb_file = 'emb_dict.pkl'
# save_file(emb_file, make_embeddings_dict(glove_50d))
emb_dict = load_file(emb_file)
dset = Dataset(filename='all_data.csv', path=path.join(path.dirname(path.dirname(path.abspath(__file__))), 'CNN_data'))

ex = dset.bodies[0]
ex = remove_punc(ex)
ex = remove_stopwords(ex)
ex = lemmatize(ex)
print(ex)

empty_array = [0]*50

def load_data():
    dset = Dataset()
    all_title_embeddings = []
    for title in dset.titles:

        title_embeddings = []
        for word in title:
            # word = word.lower()
            print(word)
            if not emb_dict.get(word) is None:
                title_embeddings.append(emb_dict.get('unk')) # POTENTIALLY CHANGE WHAT TO APPEND
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
            body_embeddings.append(emb_dict[word])
        
        if len(body_embeddings) > 500:
            body_embeddings = body_embeddings[:500]
        elif len(body_embeddings) < 500:
            while len(body_embeddings) < 500:
                body_embeddings.append(empty_array)

        all_body_embeddings.append(body_embeddings)

    train_title = all_title_embeddings[:int(len(all_title_embeddings) * 0.75)]
    test_title = all_title_embeddings[int(len(all_title_embeddings) * 0.75):]
    train_body = all_body_embeddings[:int(len(all_body_embeddings) * 0.75)]
    test_body = all_body_embeddings[int(len(all_body_embeddings) * 0.75):]
    train_labels = dset.labels[:int(len(all_body_embeddings) * 0.75)]
    test_labels = dset.labels[int(len(all_body_embeddings) * 0.75):]

    return train_title, test_title, train_labels, train_body, test_body, test_labels
