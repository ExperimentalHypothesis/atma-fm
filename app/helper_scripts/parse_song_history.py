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
    """ create playlist from log file, to be printed on frontend """

    import collections
    Song_details = collections.namedtuple('Song_details',['played_at', 'author', 'album', 'title'])

    song_history = []
    path_to_file =  r"C:\Users\nirvikalpa\Desktop\playlist.txt"
    with open(path_to_file) as playlist:
        for line in list(playlist)[-n:]:
            if "Rotating queues and looping again..." in line:
                   continue
            else:
                # new_line = line.replace("2020: Now playing ", '-- ').strip(".mp3\n").lower().split(' -- ')
                # song_history.append(tuple(new_line))
                cleared_line = line.replace("2020: Now playing ", '-- ').strip(".mp3\n").lower().split(' -- ') # TODO regex
                print(cleared_line[1][3:])
                cleared_line[1] = cleared_line[1][3:]
                song_details = Song_details(*cleared_line)
                song_history.append(song_details)
    return(reversed(song_history))

# songs = get_last_n_songs(10)
# print(songs)

