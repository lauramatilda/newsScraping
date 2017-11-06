#import scrapy
import urllib
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.news
articles = db.articles

def fetch_page(url):
    return urllib.urlopen('http://www.dailymail.co.uk/' + url).read()

def fetch_article_list(url):
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    html_articles = soup.find('ul', class_='archive-articles').find_all('a')
    for html_article in html_articles:
        article = {
            'publication': 'daily_mail',
            'url': html_article['href'],
            'title': html_article.get_text()
        }
        articles.insert_one(article)

def fetch_article_detail(url):
    html = fetch_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    article_body = soup.find('div', itemprop='articleBody')
    text = ''
    html_paras = article_body.find_all('p')
    for html_para in html_paras:
        text += html_para.get_text() + '\n'
    #article = articles.find_one({url: url})
    #print article
    print text.strip()

#ARCHIVE_PAGE = 'http://www.dailymail.co.uk/home/sitemaparchive/day_20171101.html'
#fetch_article_list(ARCHIVE_PAGE)

DETAIL_PAGE = 'http://www.dailymail.co.uk/'
fetch_article_detail('/tvshowbiz/article-5041165/Is-Lara-Bingle-Gwyneth-Paltrow.html')
