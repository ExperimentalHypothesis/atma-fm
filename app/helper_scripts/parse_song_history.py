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


def get_last_n_songs(n: int) -> list:
    import collections, re
    Song_details = collections.namedtuple('Song_details',['played_at', 'author', 'album', 'title'])
    song_history = []
    p= r'C:\Users\nirvikalpa\Desktop\playlist.txt'
    path_to_file =  r"/var/log/icecast/song-history.log"
    try:
        with open(path_to_file) as playlist:
            for line in list(playlist)[-20:]:
                # print(line)
                if "Now playing" not in line:
                    continue
                else:
                    cleared_line = line.replace("2020: Now playing ", '-- ').strip(".mp3\n").lower().split(' -- ') # TODO regex
                    name = cleared_line[1].split(" ")
                    name = " ".join(name[1:])
                    album = cleared_line[3].replace(" [lame]","")
                    song_details = Song_details(cleared_line[0], name, cleared_line[2], album)
                    song_history.append(song_details)
    except Exception as e:
        print("there is no such filename")
    return(reversed(song_history[-n:]))

# songs = get_last_n_songs(8)
# for i in songs:
#     print(i)



