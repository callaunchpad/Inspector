import bert
import pandas as pd
import numpy as np
from bert import bert_tokenization
from os import path

class BertData():
    
    def __init__(self):
        max_seq_len = 128
        title_col = 'title'
        text_col = 'text'
        label_col = 'type'
        model_dir = path.join(path.dirname(path.abspath(__file__)), 'uncased_L-12_H-768_A-12')
        cnndata_dir = path.join(path.dirname(path.dirname(path.abspath(__file__))), 'CNN_data')

        print('loading bert data...')
        train_data = pd.read_csv(path.join(cnndata_dir, 'all_data.csv'))
        tokenizer = bert_tokenization.FullTokenizer(vocab_file=path.join(model_dir, "vocab.txt"))
        input_tokens = []
        input_labels = []

        print('tokenizing bert data...')
        for _, row in train_data.iterrows():
            text, title, label = row[text_col], row[title_col], row[label_col]
            total_text = text + title
            
            tokens = tokenizer.tokenize(total_text)
            tokens = ["[CLS]"] + tokens + ["[SEP]"]
            token_ids = tokenizer.convert_tokens_to_ids(tokens)
            token_ids = token_ids[:min(len(token_ids), max_seq_len)]
            token_ids = token_ids + [0] * (max_seq_len - len(token_ids))
            
            input_tokens.append(token_ids)
            if (label == 'real'):
                input_labels.append(1)
            elif (label == 'fake'):
                input_labels.append(0)
            
        print('loaded and processed bert data!')

        doubles = list(zip(input_tokens, input_labels))
        np.random.shuffle(doubles)
        input_tokens, input_labels = zip(*doubles)
        print('shuffled bert data')

        self.train_data = np.array(input_tokens[:int(len(input_tokens) * 0.75)])
        self.test_data = np.array(input_tokens[int(len(input_tokens) * 0.75):])
        self.train_labels = np.array(input_labels[:int(len(input_labels) * 0.75)])
        self.test_labels = np.array(input_labels[int(len(input_labels) * 0.75):])
        self.max_seq_len = max_seq_len
