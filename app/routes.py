import requests
from app import app
from flask import render_template, Response
import random, time, os, random

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
	song_history= [("jun 13, 08:32 2020", "steve roach", "structures of silence", "early man"),
					("jun 13, 08:43 2020", "robert rich", "amala", "rainforest"),
					("jun 13, 08:56 2020", "ambientum", "silence is noisy", "creative"),
					("jun 13, 09:34 2020", "voice of eye", "rubadurs", "voice in the air"),]*3
	return render_template("playlist.html", song_history=song_history)

