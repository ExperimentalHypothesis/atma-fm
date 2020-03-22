"""
# NAMING PATTERNS OF AUDIOFILE THAT I HAVE FOUND :                                      REGEX:                                  GET NAME:

01 imperium i.mp3                                                                   ^\d\d\s[\w+\s().,:'?!\[\]]*$                     " ".join(s.split()[1:])
11 the blue gates of death (before and beyond them).mp3                             ^\d\d\s[\w+\s().,:'?!\[\]]*$                     " ".join(s.split("-")[1:])

2 07 they return to their earth (they are dead).mp3                                 ^\d\s\d\d\s[\w+\s().,:'?!\[\]]*$  
2 07 they return to their earth.mp3                                                 ^\d\s\d\d\s[\w+\s().,:'?!\[\]]*$               " ".join(s.split(" - ")[1:])

01 , part one.mp3                                                                   ^\d\d\s[,]\s[\w\s()]*.mp3                   " ".join(s.split(" - ")[1:])
01 , part one (and the end).mp3    


09 who'll fall
04 rome for douglas p.
10 [untitled]
03 tokyo a.m.
1 06 new fool's moon the closet
1 07 my wandering star as a bird, part 2
03 six hours to louisiana, black coffee going cold
07 elvis on the radio, steel guitar in my soul
08 3 a.m. somewhere out of beaumont
01 first, consider the lillies
04 4am exhale (chill out, world!)
04 montagne d'or (der gute berg)
05 oxbow lakes (andy's space mix)

"""
##############################################################################################################################################################

# some files have in the name of song also name of album and/or name of artist - these source cannot be matched with regex (or they can, but parsing out the songname)
# will be more complicated) so the solution to it is:


# steps to clear the files
# 0] get rid of all the -_ chars and make it lowercase
# 1] get rid of album name and artist name in the songname 
# 2] apply regex

# 3] parse out the name only

import os, re
from collections import namedtuple

print("importing...")


def delete_spaces(root:str) -> None:
    """ delete unnecesary spaces in song names """

    for path, dirs, files in os.walk(root):
        for file in files:
            src_file = os.path.join(path, file)
            dst_file = os.path.join(path, file.replace("   ", " ").replace("  ", " "))
            os.rename(src_file, dst_file)


def strip_out_artists_albums_names(root:str) -> None:
    """ strip out artist name and album name if they are a part of name of a song name """

    for artist_folder in os.listdir(root):
        for album_folder in os.listdir(os.path.join(root, artist_folder)):
            tracklist = [track for track in os.listdir(os.path.join(root, artist_folder, album_folder)) if track.endswith((".mp3", ".flac", ".wma"))]
            if all(artist_folder in song for song in tracklist) or all(album_folder in song for song in tracklist): 
                print(f"Album {album_folder} contains substrings as part of all audio tracks")
                for file in os.listdir(os.path.join(root, artist_folder, album_folder)):
                    src_file = file
                    dst_file = file.replace(artist_folder, "")
                    dst_file = dst_file.replace(album_folder, "")
                    print(f"renaming {src_file} to {dst_file}")
                    os.rename(os.path.join(root, artist_folder, album_folder, src_file), os.path.join(root, artist_folder, album_folder, dst_file))


# TODO pridat checky velikosti znaku - jestli uz to existuje ale pres if ZXY in path...
def normalize_artists_albums_songs_names(root:str) -> None:
    """ strip out year in album folder name, strip out and -_ char from all song names, album names, artist names and make all song names, album names, artist names lowercase -> all this leads to better parsing which comes next
    """
    # 1] rename all artist folder bottom down as u traverse
    for artist_folder in os.listdir(root):
        artist_folder_normalized = artist_folder.replace("-", " ").replace("_", " ").lower()
        src_name = os.path.join(root, artist_folder)
        dst_name = os.path.join(root, artist_folder_normalized)
        if os.path.exists(dst_name): 
            print(f"Artist {artist_folder_normalized} on path {dst_name} already exists")
            #continue
        # try:
        #     os.rename(src_name, dst_name)
        # except FileExistsError as e:
        #     print(e)
        else:
            os.rename(src_name, dst_name)
            print(f"Renaming artist from {src_name} to {dst_name}")

        #print(artist_folder_normalized)

     
        # 2] rename all album folders of each artist
        for album_folder in os.listdir(os.path.join(root, artist_folder_normalized)):
            album_folder_normalized = re.sub("^\d\d\d\d\s?\-?", "", album_folder)
            album_folder_normalized = album_folder_normalized.replace("-"," ").replace("_", " ").lower()
            src_name = os.path.join(root, artist_folder_normalized, album_folder)
            dst_name = os.path.join(root, artist_folder_normalized, album_folder_normalized)
            if os.path.exists(dst_name):
            # try:
            #     os.rename(src_name, dst_name)
            # except FileExistsError as e:
            #     print(e)
                print(f" Album {album_folder_normalized} on path {dst_name} already exists")
                #continue
            else:
                os.rename(src_name, dst_name)
                print(f"Renaming album from {src_name} to {dst_name}")

            # print("  ", album_folder_normalized)

            
            # 3] rename all tracks of each album
            for file in os.listdir(os.path.join(root, artist_folder_normalized, album_folder_normalized)):
                if file.endswith((".mp3", ".flac")):
                    file_normalized = file.replace("-", " ").replace("_", " ").lower()
                    file_normalized = re.sub("\s\s\s", " ", file_normalized)
                    src_name = os.path.join(root, artist_folder_normalized, album_folder_normalized, file)
                    dst_name = os.path.join(root, artist_folder_normalized, album_folder_normalized, file_normalized)
                    if os.path.exists(dst_name):
                        print(f"  Track {file_normalized} on path {dst_name} already exists")
                        #continue
                    else:
                        os.rename(src_name, dst_name)
                        print(f"Renaming {src_name} to {dst_name}")
                    #print("    ", file)
    
    strip_out_artists_albums_names(root)
    delete_spaces(root)



"""
01 name of song.mp3
01 name of artist -- name of album -- name of song.mp3
"""


def rename_songs_for_broadcasting(release:namedtuple) -> None:
    """ 
    renames songs used to radio broadcast following this pattern:
    old name: 01 name of song.mp3
    new name: 01 name of artist -- name of album -- name of song.mp3
    """
    album, artist, songs = release.album, release.artist, release.songs
    #print(album, artist, songs)
    

def make_tuples_of_album_artist_songs(root:str) -> None:
    """ create namedtuple from all albums in root dir in the form of artist, album, songs[] """

    #audio_extensions = os.path.join(os.path.dirname(__file__), "audio_extensions.txt")
    audio_extensions = r"C:\Users\nirvikalpa\Disk Google\coding\Python\repos\radio\app\helper_scripts\audio_extensions.txt"    
    with open(audio_extensions) as f:
        e = f.read().splitlines()

    Release = namedtuple("Release", ["artist", "album", "songs"])
    releases = []

    for artist_folder in os.listdir(root):
        for album_folder in os.listdir(os.path.join(root, artist_folder)):
            tracklist = [track for track in os.listdir(os.path.join(root, artist_folder, album_folder)) if track.endswith(tuple(e))]
            release = Release(artist_folder, album_folder, tracklist)
            rename_songs_for_broadcasting(release)
            print("printing release", release)
    #         releases.append(release)
    # return releases   


def find_regex_pattern_match(root:str) -> None:
    """ prints all audio files with particular regex pattern and parse out the song name only """

    p1 = re.compile("(^\d\d)(\s)([\w+\s().,:'?!\[\]]*)$") # one CD 
    p2 = re.compile("(^\d\s\d\d)(\s)([\w+\s().,:'?!\[\]]*)$") # multiple CD

    #audio_extensions = os.path.join(os.path.dirname(__file__), "audio_extensions.txt")
    audio_extensions = r"C:\Users\nirvikalpa\Disk Google\coding\Python\repos\radio\app\helper_scripts\audio_extensions.txt"
    with open(audio_extensions) as f:
       e = f.read().splitlines()

    for artist_folder in os.listdir(os.path.join(root)):
        for album_folder in os.listdir(os.path.join(root, artist_folder)):
            for file in os.listdir(os.path.join(root, artist_folder, album_folder)):
                if file.endswith(tuple(e)):
                    file = os.path.splitext(file)[0]
                    if p1.match(file):      print(file, " -> p1 match") # continue
                    elif p2.match(file):    print(file, " -> p2 match") # continue
                    else: print(file, " -> no regex match")


def count_albums(root:str) -> int:
    """ return number of albums i a root dir """

    c = 0
    for artist_folder in os.listdir(root):
        for album_folder in os.listdir(os.path.join(root, artist_folder)):
            c += 1
    return c


def print_all_files(root:str) -> None:
    """ print all audio files in a directory """

    for path, dirs, folders in os.walk(root):
        for file in folders:
            if file.endswith((".mp3", ".flac", ".wma")):
                print(file)


def print_dir_tree(root:str) -> None:
    """ prints directory tree of all files """

    for artist in os.listdir(root):
        print(artist)
        for album in os.listdir(os.path.join(root, artist)):
            print("  ", album)
            for file in os.listdir(os.path.join(root, artist, album)):
                print("     ", file)





def main(root:str):
    normalize_artists_albums_songs_names(root)
    find_regex_pattern_match(root)

if __name__ == "__main__":
    main(root)




