from flask import Flask, render_template, request, flash, redirect, url_for
from hashids import Hashids
from replit import db
import random
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SEC_KEY']

@app.route("/")
def home():
  return render_template("index.html")

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    list_text = text.split(",")
    auto = request.form['auto']

    if len(list_text) < 2:
      return render_template("index.html")

    if len(list_text) > 3:
      auto = "no"

    url = text.replace(" ", "")

    hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])
    url_id = len(db) + 1
    hashid = hashids.encode(url_id)
    short_url = "https://tabs.applejuicefan.repl.co/" + hashid

    db[hashid] = {"urls": str(url), "id": url_id, "auto": auto}
    return render_template("create.html", short_url=short_url)

@app.route("/<_id>")
def tabs(_id):
  try:
    link_list = db[_id]["urls"].splitlines();
    return render_template("tabs.html", links=str(db[_id]["urls"]), auto=str(db[_id]["auto"]), link_list = link_list)
  except:
    return("Failed to load data")
  else:
    return("Failed to load links")

if __name__ == "__main__":
	app.run(
		host='0.0.0.0',
		port=random.randint(2000, 9000))