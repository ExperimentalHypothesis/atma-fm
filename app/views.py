from app import app
from flask import render_template, Response
import random, time, os, random, vlc
from itertools import cycle

# folder = r"C:\Broadcast\Ambient Temple Of Imagination"
# one_album_path = r"C:\Users\nirvikalpa\Music\Ambient Temple Of Imagination\ATOI - Gaia (Vol.4) - 1996"
# one_album_playlist = [os.path.join(one_album_path, i) for i in os.listdir(one_album_path) if i.endswith(".mp3")]
# # print(random.shuffle(one_album_playlist))


root = r"C:\Broadcast\Ambient Temple Of Imagination"
playlist = []
for path, dirs, files in os.walk(root):
	for file in files:
		if file.endswith(".mp3"):
			playlist.append(os.path.abspath(os.path.join(path,file)))
random.shuffle(playlist)
print(playlist)

@app.route("/")
def main():
	return render_template("mainpage/main.html")

@app.route("/stream")
def stream():
	def gen():
		for song in cycle(playlist):
			with open(song, "rb") as f, open(f"{song}.log", "wb") as of:
				breakpoint()
				print(song) # DEBUG
				data = f.read(1024)
				while data:
					of.write(data)
					yield data
					data = f.read(1024)
	return Response(gen(), mimetype="audio/mp3")
