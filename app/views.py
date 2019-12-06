from app import app
from flask import render_template

import random, time, vlc, os, random



path = r"C:\Users\nirvikalpa\Desktop\2000 volven"
file = random.choice(os.listdir(path))
full_name = path + "\\" + file

def play_random_song(song):
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()
    media = vlc_instance.media_new(song)
    player.set_media(media)
    player.play()
    file = random.choice(os.listdir(path))
    time.sleep(1.5)
    print(f"Duration of this song is {player.get_length()/1000} seconds")
    time.sleep(player.get_length()/1000)  


""" 
while True:
    file = random.choice(os.listdir(path))
    full_name = path + "\\" + file
    print(f"currently playing {full_name}")    
    play_random_song(full_name)
 """


@app.route("/")
def hello():
	return render_template("mainpage/main.html")

@app.route("/radio")
def play_track() -> None:	
	while True:
		file = random.choice(os.listdir(path))
		full_name = path + "\\" + file
		print(f"currently playing {full_name}")    
		play_random_song(full_name)
	return render_template("radiopage/radio.html")