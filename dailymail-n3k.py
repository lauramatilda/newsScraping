import datetime
import urllib
from urllib.request import urlopen, Request
import time
from bs4 import BeautifulSoup
import json
from newspaper import Config, Article
from pymongo import MongoClient
import os

# client = MongoClient('localhost', 27017)
# db = client.news
# articles = db.articles

MONGODB_URL = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/news')

client = MongoClient(MONGODB_URL) #previously ('localhost', 27017)
db = client.get_default_database()
# db = client.news
articles = db.articles

USERAGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"

config = Config()
config.http_success_only = False
config.verbose = True
config.browser_user_agent = USERAGENT

def fetch_page(url):
    url = 'http://www.dailymail.co.uk' + url
    print(url)
    # return urllib.urlopen(url).read()
    return urlopen(url)
    # return urlopen(Request(url, headers={USERAGENT}))

def fetch_article_list(url,d):
    html = fetch_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    html_articles = soup.find('ul', class_='archive-articles').find_all('a')
    for html_article in html_articles:
        a = articles.find_one({'url': html_article['href']})
        if (('/news/' in html_article['href']) or ('/wires/' in html_article['href']) or ('/money/' in html_article['href'])):
            if a is None:
                article = {
                    'publication': 'daily_mail',
                    'method': 'n3k',
                    'url': html_article['href'],
                    'date': d,
                    'title': html_article.get_text()
                }
                articles.insert_one(article)
            else:
                print('Already indexed', html_article['href'])
        else:
            print('not relevant article', html_article['href'])

def fetch_article_detail(url,article):
    url = 'http://www.dailymail.co.uk' + url
    a = Article(url, config)
    try:
        a.download()
        time.sleep(1)
        a.parse()
    except (KeyboardInterrupt, SystemExit):
        print("!! INTERRUPT !!")
        raise
    except: #(ArticleException, RuntimeError, TypeError, NameError)
        print("!! DOWNLOAD ERROR / PASS !!")
        pass
    else:
        a.nlp()
        # article = {}
        article['fetched'] = datetime.datetime.utcnow()
        article['pubdate'] = a.publish_date
        print("FETCHED: ", article['date'], " ", url)
        article['text'] = a.text
        article['img'] = a.top_image
        # print(a.top_image)
        article['keywords'] = a.keywords
        # print(article)
        article['html'] = a.html
        articles.save(article)

def fetch_detail_loop():
    for article in articles.find():
        if 'fetched' not in article:
            fetch_article_detail(article['url'],article)
            # time.sleep(1)
            #print 'need to fetch', article['url']

def fetch_list_loop():
    datetime_start = datetime.datetime(2012, 3, 6)
    offset = 0
    while True:
        d = datetime_start + datetime.timedelta(offset)
        if d.year >= 2017:
            break
        list_url = '/home/sitemaparchive/day_%s.html' % d.strftime('%Y%m%d')
        fetch_article_list(list_url,d)
        offset += 1
        time.sleep(1)

if __name__=='__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 dailymail-n3k.py [list|detail]")
        sys.exit()
    cmd = sys.argv[1]
    if cmd == 'list':
        fetch_list_loop()
    elif cmd == 'detail':
        fetch_detail_loop()
    else:
        print("wrong command")
