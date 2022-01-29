from flask import current_app as app
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("under-construction.html.html")

@app.route("/channels")
def channels():
	return render_template("under-construction.html")

@app.route("/playlists")
def playlists():
	return render_template("under-construction.html")

@app.route("/archive")
def archive():
	return render_template("under-construction.html")

@app.route("/contact")
def contact():
	return render_template("under-construction.html")

@app.route("/support")
def support():
	return render_template("under-construction.html")