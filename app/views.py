from app import app
from flask import render_template, Response
import random, time, vlc, os, random

path = r"C:\Users\nirvikalpa\Desktop\Ambient Temple Of Imagination\MY$TERY SCHOOL\ATOI - Planetary House Nation (Vol.5) - 1997"

@app.route("/")
def main():
	return render_template("mainpage/main.html")

def gen():
	for i in os.listdir(path):
		with open(path + "\\" + i, "rb") as f:
			data = f.read(1024)
			while data:
				yield data
				data = f.read(1024)
				
@app.route("/stream")
def stream():
	return Response(gen(), mimetype="audio/mp3")
