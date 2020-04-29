
import time, subprocess, re, collections
from flask import current_app as app

# was used as a testing  module for getting song history data from remote server 

# def read_file_from_remote(host: str, user: str, pwd: str) -> list:
# 	""" reads the playlist of last n songs from remote linux server """

# 	import paramiko
# 	ssh_client = paramiko.SSHClient()
# 	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # this is to validate the clients machine
# 	try:
# 		ssh_client.connect(hostname=host, username=user, password=pwd)
# 	except Exception as e:
# 		print(e) # TODO na frontend
# 	else:
# 		song_history = []
# 		path_to_file = r"/var/log/icecast/icegen1.log"
# 		sftp_client = ssh_client.open_sftp()
# 		remote_file = sftp_client.open(path_to_file)
# 		try:
# 			for line in list(remote_file)[-7:]:
# 				song_history.append(line)
# 			return reversed(song_history) 
# 		except Exception as e:
# 			print(e) # TODO na frontend
# 		finally:
# 			remote_file.close()


# def parse_song_history(playlist: list) -> list:
# 	""" parses the playlist """

# 	parsed_list = []
# 	for line in playlist:
# 		if "Rotating queues and looping again..." in line:
# 			continue
# 		else:
# 			parsed_list.append(line.replace("2020: Now playing ", ' -- ').strip(".mp3\n").lower())
# 	return parsed_list


# def get_last_n_songs(n: int) -> list:
#     """ get last n songs from logfile playlist to be displayed at frontend """

#     Song_details = collections.namedtuple('Song_details',['played_at', 'author', 'album', 'title'])
#     song_history = []
#     p= r'C:\Users\nirvikalpa\Desktop\playlist.txt'
#     path_to_file =  r"/var/log/icecast/song-history.log"
#     try:
#         with open(path_to_file) as playlist:
#             for line in list(playlist)[-20:]:
#                 # print(line)
#                 if "Now playing" not in line:
#                     continue
#                 else:
#                     cleared_line = line.replace("2020: Now playing ", '-- ').strip(".mp3\n").lower().split(' -- ') # TODO regex
#                     name = cleared_line[1].split(" ")
#                     name = " ".join(name[1:])
#                     album = cleared_line[3].replace(" [lame]","")
#                     song_details = Song_details(cleared_line[0], name, cleared_line[2], album)
#                     song_history.append(song_details)
#     except Exception as e:
#         print("there is no such filename")
#     return(reversed(song_history[-n:]))



linux_logfile = "/var/log/icecast/song-history.log"
windows_logfile = r"C:\Users\nirvikalpa\source\repos\Python\flask-online-radio\song-history.log"

def get_last_n_records(path_to_file=linux_logfile, n=1):
    """ get last n records from log file """
    proc = subprocess.Popen(['tail', f'-n {n}', path_to_file], stdout=subprocess.PIPE)
    lines = proc.stdout.readlines()

    # for database
    if n == 1:
        return lines[-1].decode().strip()
    
    # for playlist
    else:
        decoded_lines = []
        for line in lines:
            decoded_lines.append(line.decode().strip())
        return decoded_lines


def parse_record(s:str) -> tuple:
    """ parses one record from log files """
    try:
        cleared = re.sub("\d\d\d\d: Now playing ", "", s)
        splitted = cleared.strip(" [lame].mp3").split(" -- ")
        started_at = " ".join(splitted[0].split()[0:4]).lower()
        artist = " ".join(splitted[0].split()[5:]).lower()
        album = splitted[1].lower()
        title = splitted[2].lower()
    except Exception as e:
        print(e)
    return title, artist, album, started_at



def create_playlist(records:list):
    """ parse list of records from log file """
    Song_details = collections.namedtuple('Song_details',['played_at', 'author', 'album', 'title'])
    song_history = []

    for i in records:
        if "Now playing" not in i:
            continue
        try:
            title, artist, album, started_at = parse_record(i)  
            song = Song_details(started_at, artist, album, title)
            song_history.append(song)
        except Exception as e:
            print(e, i)
    return song_history


if __name__ == "__main__":



    song_history = create_playlist(records)
    song_history.reverse()
    print(song_history)
