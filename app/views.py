import requests
from app import app
from flask import render_template, Response
import random, time, os, random, vlc
from itertools import cycle

prefix = r"static/audio/"
folder = r"C:\Users\nirvikalpa\source\repos\radio\app\static\audio"
one_album_path = r"C:\Users\nirvikalpa\source\repos\radio\app\static\audio"
one_album_playlist = [(prefix + i) for i in os.listdir(one_album_path) if i.endswith(".mp3")]
print(random.shuffle(one_album_playlist))

# root = r"C:\Broadcast\Ambient Temple Of Imagination"
# playlist = []
# for path, dirs, files in os.walk(root):
# 	for file in files:
# 		if file.endswith(".mp3"):
# 			playlist.append(os.path.abspath(os.path.join(path,file)))
# random.shuffle(playlist)
# print(playlist)

@app.route("/")
def main():
	return render_template("mainpage/main.html")

# @app.route("/stream")
# def stream():
# 	def gen():
# 		for song in cycle(playlist):
# 			with open(song, "rb") as f, open(f"{song}.log", "wb") as of:
# 				#breakpoint()
# 				print(song) # DEBUG
# 				data = f.read(1024)
# 				while data:
# 					of.write(data)
# 					yield data
# 					data = f.read(1024)
# 	return Response(gen(), mimetype="audio/mp3")

# def gen():
# 	# for song in cycle(playlist):
# 	song = random.choice(playlist)
# 	with open(song, "rb") as f, open(f"{song}.log", "wb") as of:
# 		#breakpoint()
# 		print("currently playing :", song) # DEBUG
# 		data = f.read(1024)
# 		while data:
# 			of.write(data)
# 			yield data
# 			data = f.read(1024)

			

# @app.route("/stream")
# def stream():
# 	return Response(gen(), mimetype="audio/mp3")
