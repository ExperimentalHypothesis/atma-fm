from app import app
from flask import render_template
import miniaudio, os

@app.route("/")
def hello():
	return render_template("mainpage/main.html")



def play():
	# stream = miniaudio.stream_file(send_from_directory("app\static\audio" ,"09_Volven_-_Your_World_In_My_Eyes.mp3"))
	stream = miniaudio.stream_file(r"C:\Users\nirvikalpa\source\repos\radio\app\static\audio\09_Volven_-_Your_World_In_My_Eyes.mp3")
	device = miniaudio.PlaybackDevice()
	device.start(stream)

@app.route("/radio")
def play_track() -> None:
	play()
	return render_template("radiopage/radio.html")