import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from nlp_tools import make_embeddings_dict, save_file, load_file, remove_punc, remove_stopwords, lemmatize
emb_file = 'emb_dict.pkl'

def search(word):
    news_url = "http://news.google.com/news?q={0}&hl=en&prmd=imvns&um=1&ie=UTF-8&output=rss".format(word)
    Client = urlopen(news_url)
    xml_page = Client.read()
    Client.close()
    soup_page = soup(xml_page,"xml")
    news_list = soup_page.findAll("item")

    article = news_list[0]
    article_link = article.link.text

    Article_Client = urlopen(article_link)
    art_xml_page = Article_Client.read()
    Article_Client.close()
    art_soup_page = soup(xml_page, "xml")
    article_text = art_soup_page.get_text()

    article_text_parsed = parse_text(article_text)
    article_text_embeddings = word_embeddings(article_text_parsed)

    return article_text_embeddings, article_link

def parse_text(text):
    no_punctuation = remove_punc(text)
    no_stopwords = remove_stopwords(no_punctuation)
    lemmatized = lemmatize(no_stopwords)
    return lemmatized

def word_embeddings(text):
        emb_dict = load_file(emb_file)
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

print(search("corona"))
