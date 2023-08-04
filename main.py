# ---- YOUR APP STARTS HERE ----
# This is the menu/controller!!

# -- Import section --
from flask import Flask
from flask import render_template
from flask import request
import model
import requests

# -- Initialization section --
app = Flask(__name__)

# -- Routes section --

# INDEX
# Routes = Locations in url
@app.route('/')
@app.route('/index')
def index():
  user = {
    "name":"Ta'Ziyah",
    "title":"Taz's really cool website"
  }
  return render_template("index.html", user=user)

@app.route('/about_us')
def about_us():
  return render_template("about_us.html")


@app.route("/results", methods = ["GET", "POST"])
def results():
  artist = request.form['artist']
  number = int(request.form['number'])
  # breakfast = request.form['breakfast']
  # rating = model.breakfast_rating(breakfast)
  # print(breakfast)
  if request.method == 'GET':
    return "<h1>Please do the form</h1>"
  if number > 10:
    return "<h1>Enter a new value please</h1>"
  else: 
    # print(request.form['nickname'])
    related_names = model.getNames(artist, number)
    related_genres = model.getGenres(artist, number)
    related_images = model.getImages(artist, number)
    related_links = model.getLinks(artist, number)
    return render_template("results.html", artist=artist, related_names = related_names, related_genres = related_genres, related_images = related_images, number = number, related_links = related_links)







# Do not delete
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
