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

# Hosting your own MongoDB

* Get a server at DigitalOcean.
* Create a server according to [these instructions](https://www.digitalocean.com/community/tutorials/how-to-use-the-mongodb-one-click-application).
* ssh login as root to the server with your account details: `ssh root@YOURIPADDRESS`
* Turn off the firewall using `ufw disable`.
* Use `nano /etc/mongod.conf` and set bindIp to `0.0.0.0`.
* Restart MongoDB using `service mongod restart`
* You can now access the MongoDB service remotely using `mongodb://YOURIP:27017/news`

# Running the scraper on a Linux VPS



    sudo apt-get install python3-pip
    sudo apt-get install python3-dev
    sudo apt-get install python3-virtualenv
    sudo apt-get install libxml2-dev libxslt-dev
    sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev

    git clone https://github.com/lauramatilda/newsScraping.git
    cd newsScraping
    virtualenv -p /usr/bin/python3 venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python3

    python dailymail-n3k.py list


# Documentation

* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [PyMongo](https://api.mongodb.com/python/current/tutorial.html)
* [Flask](http://flask.pocoo.org/docs/0.12/)
* [12-factor app](https://12factor.net/)
* [Jinja Templating](http://jinja.pocoo.org/docs/2.10/)
* [Python apps on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
