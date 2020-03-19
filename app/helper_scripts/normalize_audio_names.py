import os, re

# HERE ARE ALL THE NAMING PATTERNS OF AUDIOFILE THAT I HAVE FOUND :                     REGEX:                                  GET NAME:

#   01 steps to heaven (new ver).mp3                                                    \d\d\s[\w\s\()]*.mp3                    " ".join(s.split()[1:])
#   01-Sudden Infant Death Syndrome.mp3                                                 \d\d-[\w\s\()]*.mp3                     " ".join(s.split("-")[1:])
#   01 - Untitled to x.mp3                                                              \d\d\s[-]\s[\w\s\()]*.mp3               " ".join(s.split(" - ")[1:])
#   (01) reflecting world.mp3                                                           \(\d\d\)\s[\w\s\()]*.mp3                " ".join(s.split()[1:])
#   1 - the rim of the pit.mp3                                                          \d\s[-]\s[\w\s\()]*.mp3                 " ".join(s.split(" - ")[1:])
#   101-blue drones for a ballad (part one).mp3                                         \d\d\d[-][\w\s\()]*.mp3                 " ".join(s.split("-")[1:])
#   01. the quiet shores.mp3                                                            \d\d[.][\w\s\()]*.mp3                   " ".join(s.split()[1:])
#   2- spoke speak.mp3                                                                  \d[-]\s[\w\s\()]*.mp3                   " ".join(s.split()[1:])


def find_regex_pattern_match(root:str) -> None:
    """ prints all audio files with particular regex pattern """

    p1 = re.compile("\d\d\s[\w\s\()]*")
    p2 = re.compile("\d\d-[\w\s\()]*")
    p3 = re.compile("\d\d\s[-]\s[\w\s\()]*")
    p4 = re.compile("\(\d\d\)\s[\w\s\()]*")
    p5 = re.compile("\d\s[-]\s[\w\s\()]*")
    p6 = re.compile("\d\d\d[-][\w\s\()]*")
    p7 = re.compile("\d\d[.][\w\s\()]*")
    p8 = re.compile("\d[-]\s[\w\s\()]*")

    audio_extensions = os.path.join(os.path.dirname(__file__), "audio_extensions.txt")
    with open(audio_extensions) as f:
       e = f.read().splitlines()

    for artist_folder in os.listdir(os.path.join(root)):
        for album_folder in os.listdir(os.path.join(root, artist_folder)):
            for file in os.listdir(os.path.join(root, api_folder, artist_folder)):
                if file.endswith(e):
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



for artist_folder in os.listdir(root):
    """ 
    find out all files of a particular album, that has songs which contain artistname  or albumname as substring:
    tales of hidden algebra (01) reflecting world.mp3 
    tales of hidden algebra (02) sunrise nebula.mp3
    etc..

    tales of hidden algebra is actually name of album, this substring is stripped out, sot that it will stay like this:
    (01) reflecting world.mp3 
    (02) sunrise nebula.mp3
    """

    audio_extensions = os.path.join(os.path.dirname(__file__), "audio_extensions.txt")
    with open(audio_extensions) as f:
       e = f.read().splitlines()

    #TODO nacist file s koncovkama, vytvorit list s nima, udelat poradek s velikost title/lower a matchovat oproti tomu 
    artist_name = artist_folder.title()
        for album_folder in os.listdir(os.path.join(root, artist_folder)):
            if "api match" in album_folder:
                album_name = album_folder.split(r"[")[0]
            album_name = re.sub("\d\d\d\d", "", album_name).title().strip()
            tracklist = [song_name for song_name in os.listdir(os.path.join(root, artist_folder, album_folder))]
            if all(album_name.lower() in song_name.lower() for song_name in tracklist) 
            or all(artist_name.lower() in song_name.lower() for song_name in tracklist):
                for song_name in os.listdir(os.path.join(root, artist_folder, album_folder)):
                    #print(os.path.join(root, artist_folder, album_folder, song_name))
                    src_name = os.path.join(root, artist_folder, album_folder, song_name)
                    song_name = os.path.basename(src_name).replace(album_name.lower(), "").replace(artist_name.lower(), "")
                    dst_name = os.path.join(root, artist_folder.title(), album_folder, s_name.lower())
                    if not os.path.exists(dst_name):
                        print(f"renaming {src_name} to {dst_name}")
                        os.rename(src_name, dst_name)








