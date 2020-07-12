import subprocess, re, collections, os
from flask import current_app as app


def get_last_n_records(path_to_file: str, n=1):
    """ Get last N records from song-history.log file. """
    path_to_file = app.config["LINUX_LOG_PATH"]
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


def parse_record(s: str) -> tuple:
    """ Parse single record from song-history.log file. """
    try:
        cleared = re.sub(r"\d\d\d\d: Now playing ", "", s)
        splitted = cleared.strip(" [lame].mp3").split(" -- ")
        started_at = " ".join(splitted[0].split()[0:4]).lower()
        artist = " ".join(splitted[0].split()[5:]).lower()
        album = splitted[1].lower()
        title = splitted[2].lower()
    except Exception as e:
        print(e)
    return title, artist, album, started_at


def create_playlist(records: list) -> list:
    """ Parse multiple of records from song-history.log file. """
    Song_details = collections.namedtuple('Song_details', ['played_at', 'author', 'album', 'title'])
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