from flask import Flask, render_template
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

MONGODB_URL = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/news')

client = MongoClient(MONGODB_URL) #previously ('localhost', 27017)
mongo_db = client.get_default_database()
db = client.news
articles = db.articles

app = Flask(__name__)

@app.route("/")
def hello():
    article_list = articles.find({
    'publication':'daily_mail',
    'url': {"$regex": "^/news/"},
    "$or": [{"title": {"$regex": ".*immigrant.*"}}, {"title": {"$regex": ".*migrant.*"}}]
    })[:500]
    return render_template('article_list.html', articles=article_list)

@app.route('/article/<article_id>')
def article_detail(article_id):
    article = articles.find_one({'_id': ObjectId(article_id)})
    return render_template('article_detail.html', article=article)

# @app.route("/")
# def jsonnify():
#     article_list = articles.find({'publication': 'daily_mail'})
#     return json.dumps('article_list.json', articles=article_list)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
