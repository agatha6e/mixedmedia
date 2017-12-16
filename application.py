from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp


import requests
import json


# Configure application
app = Flask(__name__)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/articles_left")
def articlesl(keyword):
    """Returns articles from left leaning media"""

    # list of left leaning media
    medialist_left = "abcnews.go.com,bloomberg.com,nytimes.com,cbsnews.com,politico.com,huffingtonpost.com,msnbc.com"

    # url for API search
    left_url = ('https://newsapi.org/v2/everything?q='+keyword+'&domains='+medialist_left+'&sortBy='+'publishedAt'+'&language=en'+'&apiKey=666aaf2f4b3246958aee5eed64c1033e')

    # request articles through API
    l = requests.get(left_url)

    # generate json dict of articles
    med_left = l.json()

    linklist_left = med_left['articles']

    return linklist_left


@app.route("/articles_right")
def articlesr(keyword):
    """Returns articles from right leaning media"""

    # list of right leaning media
    medialist_right = "foxnews.com,nypost.com,wsj.com,washingtontimes.com,breitbart.com,forbes.com"

    # URL for API search
    right_url = ('https://newsapi.org/v2/everything?q='+keyword+'&domains='+medialist_right+'&sortBy='+'publishedAt'+'&language=en'+'&apiKey=666aaf2f4b3246958aee5eed64c1033e')

    # request articles through API
    r = requests.get(right_url)

    # generates json list of articles
    med_right = r.json()

    # generate json dict of articles
    linklist_right = med_right['articles']

    return linklist_right


@app.route("/", methods=["GET", "POST"])
def index():
    """Search keyword"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # register keyword from form
        keyword = request.form.get("keyword")

        # request articles based on keywords
        left_list = articlesl(keyword)
        right_list = articlesr(keyword)

        # Return search columns
        return render_template("results.html", keyword=keyword, left_list=left_list, right_list=right_list)

    # User reached route via GET (as by clicking a link or via redirect)
    # Initial search page
    else:
        return render_template("search.html")

