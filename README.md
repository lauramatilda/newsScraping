# Setting up (macOS)

Install [Homebrew](https://brew.sh/). Then install MongoDB:

    brew install mongodb

In the Terminal, install pip / virtualenv

    sudo easy_install pip virtualenv

Download the project and make a new virtual environment

    git clone https://github.com/lauramatilda/newsScraping.git
    cd newsScraping
    virtualenv venv

Activate the virtual environment and install the dependencies:

    source venv/bin/activate
    pip install -r requirements.txt

# Development

Open a terminal to start MongoDB, and keep it running:

    mongod --config /usr/local/etc/mongod.conf

In a different terminal tab, `cd` to the project directory and activate the virtual environment:

    cd newsScraping
    source venv/bin/activate

To run the Daily Mail scraper:

    python dailymail.py

To run the Flask server:

    export FLASK_APP=server.py
    export FLASK_DEBUG=1
    flask run

# Documentation

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [PyMongo](https://api.mongodb.com/python/current/tutorial.html)
* [Flask](http://flask.pocoo.org/docs/0.12/)
