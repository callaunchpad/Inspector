import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse
from nlp_tools import make_embeddings_dict, save_file, remove_punc, remove_stopwords, lemmatize
import time

def search(query, emb_dict):
    print("search beginning...")
    print("search query:", query)
    articles_info = googleSearch(query)
    result = []
    print("article_info length:", len(articles_info))
    for text, link in articles_info:
        text = text[:500]
        # print(link)
        # print("text", word_embeddings(text, emb_dict))
        result.append((word_embeddings(text, emb_dict), link))
    # print(result)
    return result
    
def googleSearch(query):
    print('googleSearch query:', query)
    url = 'https://www.bing.com/news/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)
    print('url:', url)
    res = requests.get(url)
    soup = BeautifulSoup(res.content, features='lxml')
    # print("soup printed:", soup)

    result = []
    links = []
    
    for link in soup.find_all("a",href=re.compile("(htt.*://.*)")):
        urls = re.split(":(?=http)",link["href"].replace("/url?q=",""))
        urls = [url.split("&sa=U&ved")[0] for url in urls]
        links.extend(urls)
    print("4 links:", links[:4])

    i = 0
    while len(result) < 4 and i < len(links): #returns first 4 links in the google search
        print("while loop started...")
        processed_link = process_url(links[i])
        if len(processed_link) != 0:
            result.append((processed_link, links[i]))
        i += 1

    print("search length:", len(result))

    return result 

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

    # print(output)
    return output

# emb_dict = load_file('../models/emb_dict.pkl')
# search('Coronavirus Live Updates: As Economy Hemorrhages Jobs, Europeans Agree to Prime E.U.’s Pump - The New York Times', emb_dict)
