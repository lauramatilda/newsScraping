import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

from flask import Flask, render_template, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

MONGODB_URL = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/news')

client = MongoClient(MONGODB_URL) #previously ('localhost', 27017)
db = client.get_default_database() #previously db = client.news
articles = db.articles

app = Flask(__name__)
app.config['DEBUG'] = False

@app.route("/")
def index():
    article_list = articles.find({
    'publication':'daily_mail',
    'url': {"$regex": "^/news/"}
    })[:50]
    return render_template('article_list.html', articles=article_list)

@app.errorhandler(500)
def page_not_found(error):
    return 'This page does not exist', 500

@app.route("/fetched")
def article_list_fetched():
    article_list = articles.find(
    {"fetched": {"$exists": 1}}
    )[:50]
    return render_template('article_list.html', title="All fetched", articles=article_list)

@app.route("/news")
def article_list_news():
    article_list = articles.find({
    'publication':'daily_mail',
    'url': {"$regex": "^/news/"},
    "$or": [{"title": {"$regex": ".*immigrant.*"}}, {"title": {"$regex": ".*migrant.*"}}]
    })[:50]
    return render_template('article_list.html', title="titles containing \"immigrant\" or \"migrant\"", articles=article_list)

@app.route('/article/<article_id>')
def article_detail(article_id):
    article = articles.find_one({'_id': ObjectId(article_id)})
    return render_template('article_detail.html', article=article)

@app.route('/api')
def api_index():
    possible_urls = ['/api/fulltext', '/api/keywords', '/api/test']
    return json.dumps(possible_urls)

@app.route('/api/fulltext')
def api_fulltext():
    query = {}
    publication = request.args.get('publication')
    if publication is not None:
        query['publication'] = publication
    article_list = articles.find(query)[:50]
    return apiResponse(list(article_list)) #json.dumps(list(article_list), cls=JSONEncoder)

@app.route('/api/<pubName>/<year>/<month>')
def api_query(pubName, year, month):
    start = datetime(int(year), int(month), 1)
    end = start + relativedelta(months=1)
    article_list = articles.find({
    'publication': pubName,
    'text': {"$exists": 1},
    'date': {"$gte" : start, "$lt": end}
    })[:250] #Have to limit due to slow server response
    text_set = []
    for article in article_list:
        text_set.append(article['text'])
    return apiResponse(list(text_set))

def apiResponse(data):
    headers = [["Access-Control-Allow-Origin", "*"]]
    return (json.dumps(data, cls=JSONEncoder), 200, headers)

@app.route('/api/keywords')
def api_keywords():
    query = {}
    publication = request.args.get('publication')
    if publication is not None:
        query['publication'] = publication
    query['keywords'] = {'$exists': 1}
    article_list = articles.find(query)[:50]
    keyword_set = set()
    for article in article_list:
        keyword_set.update(article['keywords'])
    return apiResponse(list(keyword_set))

# @app.route("/")
# def jsonnify():
#     article_list = articles.find({'publication': 'daily_mail'})
#     return json.dumps('article_list.json', articles=article_list)

@app.template_filter()
def nl2br(s):
    return s.replace('\n', '<br>')

@app.template_filter()
def squeeze_breaks(s):
    return s.replace('<br><br>', '<br>')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
