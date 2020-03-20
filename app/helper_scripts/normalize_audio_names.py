import os, re

# NAMING PATTERNS OF AUDIOFILE THAT I HAVE FOUND :                                      REGEX:                                  GET NAME:

#   01 steps to - heaven (new ver).mp3                                                    \d\d\s[\w\s\()\-]*.mp3                    " ".join(s.split()[1:])
#   01-Sudden Infant Death Syndrome.mp3                                                 \d\d-[\w\s\()\-]*.mp3                     " ".join(s.split("-")[1:])
#   01  Untitled to x.mp3                                                              \d\d\s[-]\s[\w\s\()\-]*.mp3               " ".join(s.split(" - ")[1:])
#   (01) reflecting world.mp3                                                           \(\d\d\)\s[\w\s\()\-]*.mp3                " ".join(s.split()[1:])
#   1  the rim of the pit.mp3                                                          \d\s[-]\s[\w\s\()\-]*.mp3                 " ".join(s.split(" - ")[1:])
#   101 blue drones for a ballad (part one).mp3                                         \d\d\d[-][\w\s\()\-]*.mp3                 " ".join(s.split("-")[1:])
#   01. the quiet shores.mp3                                                            \d\d[.][\w\s\()\-]*.mp3                   " ".join(s.split()[1:])
#   2 spoke speak.mp3                                                                  \d[-]\s[\w\s\()\-]*.mp3                   " ".join(s.split()[1:])

# some files have in the name of song also name of album and/or name of artist - these source cannot be matched with regex (or they can, but parsing out the songname)
# will be more complicated) so the solution to it is:

# steps:
# 0] get rid of all the - chars nad make it lowercase
# 1] get rid of album name in the songname
# 2] get rig of artist name in the songname
# 3] apply regex and parse out




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
        #if not os.path.exists(dst_name):
        print(f"renaming artist from {src_name} to {dst_name}")
        os.rename(src_name, dst_name)
        print(artist_folder_normalized)
        
        # 2] rename all album folders of each artist
        for album_folder in os.listdir(os.path.join(root, artist_folder_normalized)):
            album_folder_normalized = re.sub("^\d\d\d\d\s?\-?", "", album_folder)
            album_folder_normalized = album_folder_normalized.replace("-"," ").replace("_", " ").lower()
            src_name = os.path.join(root, artist_folder_normalized, album_folder)
            dst_name = os.path.join(root, artist_folder_normalized, album_folder_normalized)
            #if album_folder_normalized not in dst_name:
            print(f"renaming album from {src_name} to {dst_name}")
            os.rename(src_name, dst_name)
            print("  ", album_folder_normalized)
            
            # 3] rename all tracks of each album
            for file in os.listdir(os.path.join(root, artist_folder_normalized, album_folder_normalized)):
                if file.endswith((".mp3", ".flac")):
                    file_normalized = file.replace("-", " ").replace("_", " ").lower()
                    file_normalized = re.sub("\s\s\s", " ", file_normalized)
                    src_name = os.path.join(root, artist_folder_normalized, album_folder_normalized, file)
                    dst_name = os.path.join(root, artist_folder_normalized, album_folder_normalized, file_normalized)
                    #if not os.path.exists(dst_name):
                    print(f"renaming {src_name} to {dst_name}")
                    os.rename(src_name, dst_name)
                    print("    ", file)
    
    strip_out_artists_albums_names(root)
    delete_spaces(root)


def find_regex_pattern_match(root:str) -> None:
    """ prints all audio files with particular regex pattern and parse out the song name only """

    p1 = re.compile("\d\d\s[\w\s\()\-]*")
    p2 = re.compile("\d\d-[\w\s\()\-]*")
    p3 = re.compile("\d\d\s[-]\s[\w\s\()\-]*")
    p4 = re.compile("\(\d\d\)\s[\w\s\()\-]*")
    p5 = re.compile("\d\s[-]\s[\w\s\()\-]*")
    p6 = re.compile("\d\d\d[-][\w\s\()\-]*")
    p7 = re.compile("\d\d[.][\w\s\()\-]*")
    p8 = re.compile("\d[-]\s[\w\s\()\-]*")

    #audio_extensions = os.path.join(os.path.dirname(__file__), "audio_extensions.txt")
    audio_extensions = r"C:\Users\nirvikalpa\Disk Google\coding\Python\repos\radio\app\helper_scripts\audio_extensions.txt"
    with open(audio_extensions) as f:
       e = f.read().splitlines()

    for artist_folder in os.listdir(os.path.join(root)):
        for album_folder in os.listdir(os.path.join(root, artist_folder)):
            for file in os.listdir(os.path.join(root, artist_folder, album_folder)):
                if file.endswith(tuple(e)):
                    file = file.replace("-", " ")
                    if p1.match(file): print(file, " -> p1 match")
                    elif p2.match(file): print(file, " -> p2 match")
                    elif p3.match(file): print(file, " -> p3 match")
                    elif p4.match(file): print(file, " -> p4 match")
                    elif p5.match(file): print(file, " -> p5 match")
                    elif p6.match(file): print(file, " -> p6 match")
                    elif p7.match(file): print(file, " -> p7 match")
                    elif p8.match(file): print(file, " -> p8 match")

                    else: print(file, " - no regex match")


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




# for artist_folder in os.listdir(root):
#     """ 
#     find out all files of a particular album, that has songs which contain artistname  or albumname as substring:
#     tales of hidden algebra (01) reflecting world.mp3 
#     tales of hidden algebra (02) sunrise nebula.mp3
#     etc..

#     tales of hidden algebra is actually name of album, this substring is stripped out, sot that it will stay like this:
#     (01) reflecting world.mp3 
#     (02) sunrise nebula.mp3
#     """

#     audio_extensions = os.path.join(os.path.dirname(__file__), "audio_extensions.txt")
#     with open(audio_extensions) as f:
#        e = f.read().splitlines()

#     #TODO nacist file s koncovkama, vytvorit list s nima, udelat poradek s velikost title/lower a matchovat oproti tomu 
#     artist_name = artist_folder.title()
#         for album_folder in os.listdir(os.path.join(root, artist_folder)):
#             if "api match" in album_folder:
#                 album_name = album_folder.split(r"[")[0]
#             album_name = re.sub("\d\d\d\d", "", album_name).title().strip()
#             tracklist = [song_name for song_name in os.listdir(os.path.join(root, artist_folder, album_folder))]
#             if all(album_name.lower() in song_name.lower() for song_name in tracklist) 
#             or all(artist_name.lower() in song_name.lower() for song_name in tracklist):
#                 for song_name in os.listdir(os.path.join(root, artist_folder, album_folder)):
#                     #print(os.path.join(root, artist_folder, album_folder, song_name))
#                     src_name = os.path.join(root, artist_folder, album_folder, song_name)
#                     song_name = os.path.basename(src_name).replace(album_name.lower(), "").replace(artist_name.lower(), "")
#                     dst_name = os.path.join(root, artist_folder.title(), album_folder, s_name.lower())
#                     if not os.path.exists(dst_name):
#                         print(f"renaming {src_name} to {dst_name}")
#                         os.rename(src_name, dst_name)



root = r"Z:\Music\api\1] api match [by names]"

def main(root:str):
    normalize_artists_albums_songs_names(root)
    find_regex_pattern_match(root)

if __name__ == "__main__":
    main(root)




