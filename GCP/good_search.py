import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse
from nlp_tools import make_embeddings_dict, save_file, load_file, remove_punc, remove_stopwords, lemmatize

def search(query, emb_dict):
    urls = googleSearch(query)
    result = []
    for url in urls:
        result.append((word_embeddings(process_url(url), emb_dict), url))
        print(result[-1])
    return result
    
def googleSearch(query):
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)
    res = requests.get(url)
    soup = BeautifulSoup(res.content, features='lxml')
    links = []
    for link in soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        links.extend(re.split(":(?=http)",link["href"].replace("/url?q=","")))
    return links[:4] #returns first 4 links in the google search

def word_embeddings(text, emb_dict):
    embeddings = []
    for word in text:
        # word = word.lower()
        #print(word)
        # if the word is OOV, append the unk vector
        if emb_dict.get(word) is None:
            embeddings.append(emb_dict.get('unk')) # POTENTIALLY CHANGE WHAT TO APPEND
        else:
            embeddings.append(emb_dict.get(word))
    return embeddings

def process_url(url):
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all('p')

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'header',
        'html',
        'meta',
        'head', 
        'input',
        'script',
        'footer'
        # there may be more elements you don't want, such as "style", etc.
    ]
    # print("testing")
    # print(text)
    for t in text:
        # print(t)
        if t.parent.name not in blacklist:
            output += '{} '.format(t.get_text())

    return output