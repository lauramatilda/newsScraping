import datetime
import urllib
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.news
articles = db.articles

def fetch_page(url):
    url = 'http://www.dailymail.co.uk' + url
    print url
    return urllib.urlopen(url).read()

def fetch_article_list(url):
    html = fetch_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    html_articles = soup.find('ul', class_='archive-articles').find_all('a')
    for html_article in html_articles:
        a = articles.find_one({'url': html_article['href']})
        if a is None:
            article = {
                'publication': 'daily_mail',
                'url': html_article['href'],
                'title': html_article.get_text()
            }
            articles.insert_one(article)
        else:
            print 'already there', html_article['href']

def fetch_article_detail(url):
    html = fetch_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    article_body = soup.find('div', itemprop='articleBody')
    text = ''
    html_paras = article_body.find_all('p')
    for html_para in html_paras:
        text += html_para.get_text() + '\n'
    article = articles.find_one({'url': url})
    article['fetched'] = datetime.datetime.utcnow()
    article['text'] = text.strip()
    article['html'] = unicode(article_body)
    articles.save(article)

#ARCHIVE_PAGE = '/home/sitemaparchive/day_20171101.html'
#fetch_article_list(ARCHIVE_PAGE)


def fetch_detail_loop():
    for article in articles.find():
        if 'fetched' not in article:
            fetch_article_detail(article['url'])
            #print 'need to fetch', article['url']



#DETAIL_PAGE = 'http://www.dailymail.co.uk/'
#fetch_article_detail('/wires/reuters/article-5037509/Return-Manaforts-money-Democrats-demand-California-Republican.html')

#fetch_article_list('/home/sitemaparchive/day_20100101.html')
fetch_detail_loop()
