import requests
from app import app
from flask import render_template, Response
import random, time, os, random, vlc
from itertools import cycle

# prefix = r"static/audio/"
# folder = r"C:\Users\nirvikalpa\source\repos\radio\app\static\audio"
# one_album_path = r"C:\Users\nirvikalpa\source\repos\radio\app\static\audio"
# one_album_playlist = [(prefix + i) for i in os.listdir(one_album_path) if i.endswith(".mp3")]
# print(random.shuffle(one_album_playlist))

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




def parse_song_history():
    with open(r"C:\Broadcast\icegen1.log") as f:
        last_ten = list(f)[-10:]
    parsed_list = []
    for line in last_ten:
        if "Rotating queues and looping again..." in line:
            continue
        else:
            parsed_list.append(line.replace("2020: Now playing ", ' -- ').strip(".mp3\n").lower())
    return parsed_list

@app.route("/playlist")
def playlist():
		song_history = parse_song_history()
		print(song_history)
		return render_template("playlist/playlist.html", song_history=song_history)



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
