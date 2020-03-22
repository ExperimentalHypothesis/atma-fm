"""
# NAMING PATTERNS OF AUDIOFILE THAT I HAVE FOUND :                                      REGEX:                                 

01 imperium= i.mp3                                                                   ^\d\d\s[\w+\s().,#=:'?!\[\]]*$                   
11 the blue gates of death (before and beyond them).mp3                             ^\d\d\s[\w+\s().,:#='?!\[\]]*$                    
00 #Ansage



2 07 they return to their earth (they are dead).mp3                                 ^\d\s\d\d\s[\w+\s().,:#='?!\[\]]*$  
2 07 they return to their earth.mp3                                                 ^\d\s\d\d\s[\w+\s().,:#='?!\[\]]*$               



"""
##############################################################################################################################################################

# some files have in the name of song also name of album and/or name of artist - these source cannot be matched with regex (or they can, but parsing out the songname)
# will be more complicated) so the solution to it is:


# steps to clear the files
# 0] get rid of all the -_. chars and make it lowercase
# 1] get rid of album name and artist name in the songname 
# 2] apply regex
# 3] parse out the name only and tag it
# 4] rename for broadcasting

import os, re, mutagen
from collections import namedtuple

print("importing...")


def delete_spaces(root:str) -> None:
    """ delete double and triple spaces in song names """

    for path, dirs, files in os.walk(root):
        for file in files:
            src_file = os.path.join(path, file)
            dst_file = os.path.join(path, file.replace("   ", " ").replace("  ", " "))
            os.rename(src_file, dst_file)


def delete_dot_after_tracknumber(root:str) -> None:
    """ some song have this format "01. songname.mp3", this will delete the dot that makes mess for re patterns """

    for path, dirs, files in os.walk(root):
        for file in files:
            src_file = os.path.join(path, file)
            if file[2] == ".":
                file = file.replace(".","", 1)
                dst_file = os.path.join(path, file)
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
# tahle funce jede jako prvni - hodne toho ocisti, co co ne se musi ruco
def normalize_names_for_filesystem(root:str) -> None:
    """ 
    strip out year in album folder name, strip out -_. and spaces from all songs, albums and artists and make all of them lowercase 
    the goal is to have:
        clear {artist_name} in the form of plain "artist name"          => for example "steve roach" 
        clear {album_name} in the form of plain "album name"            => for example "structures of silence"
        clear {song name} in the of "song name" with track number       => for example "01 early man.mp3"
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
            if "api match" in album_folder_normalized:
                album_folder_normalized = album_folder_normalized.rsplit(" [api", 1)[0]
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
    delete_dot_after_tracknumber(root)






def tag_songs_based_on_regexes(release:namedtuple) -> None:
    """ 
    write id3 tags [artist, album, title] to audio files (used for the albums that are not found by by MusicBranz Pickard)
    artist, album and title is parsed out from filesystem using regex patterns.
    to be parsed out and renamed corretly, the names must be already normalized with normalize_artists_albums_songs_names()
    """

    p1 = re.compile("(^\d\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # one CD 
    p2 = re.compile("(^\d\s\d\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # multiple CD
    p3 = re.compile("(^\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # one CD no leading zero (1 song name.mp3)


    artist, album, songs, paths = release.artist.title(), release.album.title(), release.songs, release.paths
    if "Api Match" in album:
        album = album.rsplit(" [Api", 1)[0]

    for song, path in zip(songs, paths):
        song_name = song.rsplit(".", 1)[0].title()
        if p1.match(song_name) or p2.match(song_name) or p3.match(song_name):
            p1_match = p1.match(song_name)
            p2_match = p2.match(song_name)
            p3_match = p3.match(song_name)
            try:
                tracknumber, _, title = p1_match.groups()
            except AttributeError:
                pass
            try:
                tracknumber, _, title = p2_match.groups()
            except AttributeError:
                pass
            try:
                tracknumber, _, title = p3_match.groups()
            except AttributeError:
                pass
            try:
                tags = mutagen.File(path, easy=True)
            except Exception as e:
                print(e, f"on path {path}" )
            try:
                tags['album'] = album
                tags['artist'] = artist
                tags['title'] = title
                tags['tracknumber'] = tracknumber
            except Exception as e:
                print(e, f"path {path}")
            try:
                tags.save()
            except UnboundLocalError as e:
                print(e, f"on file {path} -> NOT TAGGED PROPERLY")
        else:
            print(f"Song {song_name} doesnt match regex -> NOT TAGGED")


#TODO
def normalize_names_for_broadcasting(release:namedtuple) -> None:
    """ rename songs used to broadcast following this pattern: 01 Name Of Artist -- Name Of Album -- Name Of Song.mp3 """

    album, artist, songs, paths = release.album, release.artist, release.songs, release.paths
    #print(album, artist, songs)

# tahle funkce jede jako druha
def tag_and_rename_songs(root:str) -> None:
    """ tag and rename song for broadcasting """

    #audio_extensions = os.path.join(os.path.dirname(__file__), "audio_extensions.txt")
    audio_extensions = r"C:\Users\nirvikalpa\Disk Google\coding\Python\repos\radio\app\helper_scripts\audio_extensions.txt"    
    with open(audio_extensions) as f:
        e = f.read().splitlines()

    Release = namedtuple("Release", ["artist", "album", "songs", "paths"])
    releases = []

    for artist_folder in os.listdir(root):
        for album_folder in os.listdir(os.path.join(root, artist_folder)):
            songs = [track for track in os.listdir(os.path.join(root, artist_folder, album_folder)) if track.endswith(tuple(e))]
            paths = [os.path.join(root, artist_folder, album_folder, track) 
                    for track in os.listdir(os.path.join(root, artist_folder, album_folder)) if track.endswith(tuple(e))]
            release = Release(artist_folder, album_folder, songs, paths)
            tag_songs_based_on_regexes(release)



def find_regex_pattern_match(root:str) -> None:
    """ prints all audio files with particular regex pattern - this is just for quick check to see matched patterns """

    p1 = re.compile("(^\d\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # one CD 
    p2 = re.compile("(^\d\s\d\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # multiple CD
    p3 = re.compile(("(^\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$")) # one CD no leading zero (1 song name.mp3)

    #audio_extensions = os.path.join(os.path.dirname(__file__), "audio_extensions.txt")
    audio_extensions = r"C:\Users\nirvikalpa\Disk Google\coding\Python\repos\radio\app\helper_scripts\audio_extensions.txt"
    with open(audio_extensions) as f:
       e = f.read().splitlines()

    for artist_folder in os.listdir(os.path.join(root)):
        for album_folder in os.listdir(os.path.join(root, artist_folder)):
            for file in os.listdir(os.path.join(root, artist_folder, album_folder)):
                if file.endswith(tuple(e)):
                    file = os.path.splitext(file)[0]
                    if p1.match(file):      print(file, " -> p1 match") 
                    elif p2.match(file):    print(file, " -> p2 match") 
                    elif p3.match(file):    print(file, " -> p3 match")
                    
                    else: print(file, " -> no regex match")


def find_no_regex_pattern_match(root:str) -> None:
    """ prints audio files that did not match any regex pattern """

    p1 = re.compile("(^\d\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # one CD leading zero (01 song name.mp3)
    p2 = re.compile("(^\d\s\d\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # multiple CD (1 01 song name.mp3)
    p3 = re.compile("(^\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # one CD no leading zero (1 song name.mp3)

    #audio_extensions = os.path.join(os.path.dirname(__file__), "audio_extensions.txt")
    audio_extensions = r"C:\Users\nirvikalpa\Disk Google\coding\Python\repos\radio\app\helper_scripts\audio_extensions.txt"
    with open(audio_extensions) as f:
       e = f.read().splitlines()

    for artist_folder in os.listdir(os.path.join(root)):
        for album_folder in os.listdir(os.path.join(root, artist_folder)):
            for file in os.listdir(os.path.join(root, artist_folder, album_folder)):
                if file.endswith(tuple(e)):
                    file = os.path.splitext(file)[0]
                    if p1.match(file): continue
                    elif p2.match(file): continue
                    elif p3.match(file): continue

                    else: 
                        print(file, " -> no regex match")
                        print(f"path: {os.path.join(artist_folder, album_folder)}")

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




test2 = r"c:\Users\nirvikalpa\Music\api\testing folder2"

if __name__ == "__main__":
    # main(root)
    tag_and_rename_songs(test2)



