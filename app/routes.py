import requests
from app import app
from flask import render_template, Response
import random, time, os, random
from app.helper_scripts.parse_song_history import get_last_n_songs
	

@app.context_processor
def pass_current_song():
	last_played = list(get_last_n_songs(1))
	# last_song.author	
	return dict(author=	last_played[0].author, title=last_played[0].title)

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/contact")
def contact():
	return render_template("contact.html")

@app.route("/archive")
def archive():
	return render_template("archive.html")

@app.route("/playlist")
def playlist():
	# song_history = parse_song_history(read_file_from_remote("167.172.122.236", "root", "emeraldincubus"))
	song_history = get_last_n_songs(14)
	return render_template("playlist.html", song_history=song_history)

