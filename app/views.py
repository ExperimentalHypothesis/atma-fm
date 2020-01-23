import requests
from app import app
from flask import render_template, Response
import random, time, os, random, vlc
from itertools import cycle

@app.route("/")
def main():
	return render_template("mainpage/main.html")



def read_file_from_remote(host: str, user: str, pwd: str) -> list:
	""" this fucntion reads the playlist of ast 25 songs from remote linux server """
	import paramiko
	ssh_client = paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # this is to validate the clients machine
	try:
			ssh_client.connect(hostname=host, username=user, password=pwd)
	except Exception as e:
			print(e) # TODO na frontend
	else:
			song_history = []
			path_to_file = r"/var/log/icecast/icegen1.log"
			sftp_client = ssh_client.open_sftp()
			remote_file = sftp_client.open(path_to_file)
			try:
					for line in list(remote_file)[-25:]:
							song_history.append(line)
					return reversed(song_history) 
			except Exception as e:
							print(e) # TODO na frontend
			finally:
					remote_file.close()


def parse_song_history(playlist: list) -> list:
	""" this function parses the playlist """
	parsed_list = []
	for line in playlist:
			if "Rotating queues and looping again..." in line:
					continue
			else:
					parsed_list.append(line.replace("2020: Now playing ", ' -- ').strip(".mp3\n").lower())
	return parsed_list

@app.route("/playlist")
def playlist():
	song_history = parse_song_history(read_file_from_remote("167.172.122.236", "root", "emeraldincubus"))
	return render_template("playlist/playlist.html", song_history=song_history)

