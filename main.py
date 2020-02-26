import embeddings
from dataset import Dataset

emb_file = 'emb_dict.pkl'
# embeddings.save_file(emb_file, embeddings.make_embeddings_dict())
emb_dict = embeddings.load_file(emb_file)
dset = Dataset()

ex = dset.articles[0]
ex = embeddings.remove_punc(ex)
ex = embeddings.remove_stopwords(ex)
ex = embeddings.lemmatize(ex)
print(ex)

