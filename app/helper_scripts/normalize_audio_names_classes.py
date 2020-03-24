import os, re, mutagen
from collections import namedtuple

print("importing..")

def get_all_audio_extensions() -> list:

    #audio_extensions = os.path.join(os.path.dirname(__file__), "audio_extensions.txt" 
    audio_extensions = r"C:\Users\nirvikalpa\Disk Google\coding\Python\repos\radio\app\helper_scripts\audio_extensions.txt"    
    with open(audio_extensions) as f:
        ext = f.read().splitlines()
    return ext

class NameNormalizer:
    """ 
    class for clearing out the names of songs, artists and albums 
    the goal is to have:
        clear {artist_name} in the form of plain "artist name"          => for example "steve roach" 
        clear {album_name} in the form of plain "album name"            => for example "structures of silence"
        clear {song name} in the of "song name" with track number       => for example "01 early man.mp3"
    """ 
    def __repr__(self):
        pass

    #TODO strip space at the end
    def strip_whitespaces(self, root:str) -> None:
        """ delete multiple spaces in song names """

        for path, dirs, files in os.walk(root):
            for file in files:
                if "  " in file or file[0] == " ":           
                    src_file = os.path.join(path, file)
                    file = re.sub(r"[\s]+", " ", file).strip()
                    dst_file = os.path.join(path, file)
                    print(f"Stripping whitespace from {src_file} --> {dst_file}")
                    os.rename(src_file, dst_file)                   
                path_file_without_ext, ext= os.path.splitext(os.path.join(path, file))
                if path_file_without_ext[-1] == " ":
                    print(f"{path_file_without_ext} has space at the end and sould be stripped")
                    # src_file = os.path.join(path, file)
                    # file = re.sub(r"[\s]+", " ", file).strip()
                    # dst_file = os.path.join(path, file)
                    # print(f"Stripping whitespace as last character {src_file} --> {dst_file}")
                    # os.rename(src_file, dst_file)                   


    def strip_dot_after_tracknumber(self, root:str) -> None:
        """ some song have this format "01. songname.mp3", this will delete the dot that makes mess for re patterns """

        for path, dirs, files in os.walk(root):
            for file in files:
                if file[2] == ".":
                    src_file = os.path.join(path, file)
                    dst_file = os.path.join(path, file.replace(".","", 1))
                    os.rename(src_file, dst_file)


    def strip_apimatch_from_album_name(self, root:str) -> None:
        """ strip [api match 131243] from album folder """

        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                if "api match" in album:
                    album_name = album.rsplit(' [api')[0]
                    src_name = os.path.join(root, artist, album)
                    dst_name = os.path.join(root, artist, album_name)
                    print(f"reaming {src_name} to {dst_name}")
                    os.rename(src_name, dst_name)


    def strip_artist_album_name_from_song(self, root:str) -> None:
        """ strip out artist name and album name if they are a part of name of a song name """

        ext = get_all_audio_extensions()

        for artist_folder in os.listdir(root):
            for album_folder in os.listdir(os.path.join(root, artist_folder)):
                tracklist = [track for track in os.listdir(os.path.join(root, artist_folder, album_folder)) if track.endswith(tuple(ext))]
                if len(tracklist) > 1 and all(artist_folder in song for song in tracklist): 
                    print(f"Album {album_folder} contains artist name '{artist_folder}' as part of all audio tracks => stripping it out..")
                    for file in os.listdir(os.path.join(root, artist_folder, album_folder)):
                        if file.endswith(tuple(ext)):
                            src_file = file
                            dst_file = file.replace(artist_folder, "", 1)
                            print(f"Renaming {os.path.join(artist_folder, album_folder, src_file)} to {os.path.join(artist_folder, album_folder, dst_file)}")
                            os.rename(os.path.join(root, artist_folder, album_folder, src_file), os.path.join(root, artist_folder, album_folder, dst_file))
                if len(tracklist) > 1 and all(album_folder in song for song in tracklist):
                    print(f"Album {album_folder} contains album name '{album_folder}' as part of all audio tracks => stripping it out..")
                    for file in os.listdir(os.path.join(root, artist_folder, album_folder)):
                        if file.endswith(tuple(ext)):
                            src_file = file
                            dst_file = file.replace(album_folder, "", 1)
                            print(f"Renaming {os.path.join(artist_folder, album_folder, src_file)} to {os.path.join(artist_folder, album_folder, dst_file)}")
                            os.rename(os.path.join(root, artist_folder, album_folder, src_file), os.path.join(root, artist_folder, album_folder, dst_file))


    def strip_parens_around_tracknumbers(self, root:str) -> None:
        """ some songs have this format: (02) Secret Light At The Upper Window """

        ext = get_all_audio_extensions()

        for path, dirs, folders in os.walk(root):
            for file in folders:
                if file.endswith(tuple(ext)):
                    if file[0] == "(" and file[3] == ")":
                        src_name = os.path.join(path, file)
                        dst_name = os.path.join(path, file.replace("(","", 1).replace(")","", 1))
                        os.rename(src_name, dst_name)
        

    def lowercase_artist(self, root:str) -> None:
        """ make artist folder lowercase """

        for artist in os.listdir(root):
            if artist != artist.lower():
                src_name = os.path.join(root, artist)
                dst_name = os.path.join(root, artist.lower())
                print(f"Lowercasing artist {src_name} to {dst_name}")
                os.rename(src_name, dst_name)


    def titlecase_artist(self, root:str) -> None:
        """ make artist folder titlecase """
        
        for artist in os.listdir(root):
            if artist != artist.title():
                src_name = os.path.join(root, artist)
                dst_name = os.path.join(root, artist.title())
                print(f"Titlecasing artist {src_name} to {dst_name}")
                os.rename(src_name, dst_name)


    def lowercase_album(self, root:str) -> None:
        """ make album folder lowercase """

        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                if album != album.lower():
                    src_name = os.path.join(root, artist, album)
                    dst_name = os.path.join(root, artist, album.lower())
                    print(f"Lowercasing album {src_name} to {dst_name}")
                    os.rename(src_name, dst_name)


    def titlecase_album(self, root:str) -> None:
        """ make album folder lowercase """

        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                if album != album.title():
                    src_name = os.path.join(root, artist, album)
                    dst_name = os.path.join(root, artist, album.title())
                    print(f"Titlecasing album {src_name} to {dst_name}")
                    os.rename(src_name, dst_name)


    def lowercase_song(self, root:str) -> None:
        """ make song name lowercase """

        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                for song in os.listdir(os.path.join(root, artist, album)):
                    if song != song.lower():
                        src_name = os.path.join(root, artist, album, song)
                        dst_name = os.path.join(root, artist, album, song.lower())
                        print(f"Lowercasing {os.path.join(artist, album, song)} ==> {os.path.join(artist, album, song.lower())}")
                        os.rename(src_name, dst_name) 


    def titlecase_song(self, root:str) -> None:
        """ make song name titlecased """

        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                for song in os.listdir(os.path.join(root, artist, album)):
                    song_name, ext = os.path.splitext(os.path.join(root, artist, album, song))
                    if song != os.path.basename(song_name.title()+ext):
                        src_name = os.path.join(root, artist, album, song)
                        dst_name = os.path.join(root, artist, album, song_name.title()+ext)
                        print(f"Titlecasing {os.path.join(artist, album, song)} ==> {os.path.join(artist, album, os.path.basename(song_name.title()+ext))}")
                        os.rename(src_name, dst_name)


    def titlecase_all(self, root:str) -> None:
        """ title all names of songs, artists, albums """

        NameNormalizer.titlecase_song(self, root)
        NameNormalizer.titlecase_album(self, root)
        NameNormalizer.titlecase_artist(self, root)


    def lowercase_all(self, root:str) -> None:
        """ lowercase all names of songs, artists, albums """

        NameNormalizer.lowercase_song(self, root)
        NameNormalizer.lowercase_album(self, root)
        NameNormalizer.lowercase_artist(self, root)

class SongTagger:

    ext = get_all_audio_extensions()

    p1 = re.compile("(^\d\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # one CD leading zero (01 song name.mp3)
    p2 = re.compile("(^\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # one CD no leading zero (1 song name.mp3)
    p3 = re.compile("(^\d\s\d\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # multiple CD (1 01 song name.mp3)
    p4 = re.compile("(^\d\d\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # multiple CD (101 song name.mp3)

    def tag_songs(self, root:str) -> None:
        """ tag songs based on regexes - the names for song, album, artist are parsed from filesystem, thus first they need to be normalized """

        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                songs = [track for track in os.listdir(os.path.join(root, artist, album)) if track.endswith(tuple(SongTagger.ext))]
                paths = [os.path.join(root, artist, album, track) 
                        for track in os.listdir(os.path.join(root, artist, album)) if track.endswith(tuple(SongTagger.ext))]
                if "api match" in album:
                    album = album.rsplit(" [api", 1)[0]
                for song, path in zip(songs, paths):
                    song_name = song.rsplit(".", 1)[0].title()
                    if SongTagger.p1.match(song_name) or SongTagger.p2.match(song_name) or SongTagger.p3.match(song_name) or SongTagger.p4.match(song_name):
                        p1_match = SongTagger.p1.match(song_name)
                        p2_match = SongTagger.p2.match(song_name)
                        p3_match = SongTagger.p3.match(song_name)
                        p4_match = SongTagger.p4.match(song_name)
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
                            tracknumber, _, title = p4_match.groups()
                        except AttributeError:
                            pass

                        try:
                            tags = mutagen.File(path, easy=True)
                        except Exception as e:
                            print(e, f"on path {path}" )

                        try:
                            tags['album'] = album.title()
                            tags['artist'] = artist.title()
                            tags['title'] = title.title()
                            tags['tracknumber'] = tracknumber
                        except Exception as e:
                            print(e, f"path {path}")

                        try:
                            tags.save()
                        except UnboundLocalError as e:
                            print(e, f"on file {path} -> NOT TAGGED PROPERLY")
                    else:
                        print(f"Song on path {path} doesnt match regex -> NOT TAGGED")

class RegexMatcher:

    ext = get_all_audio_extensions()

    p1_song = re.compile("(^\d\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # one CD leading zero (01 song name.mp3)
    p2_song = re.compile("(^\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # one CD no leading zero (1 song name.mp3)
    p3_song = re.compile("(^\d\s\d\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # multiple CD (1 01 song name.mp3)
    p4_song = re.compile("(^\d\d\d)(\s)([\w+\s().,:#=&'?!\[\]]*)$") # multiple CD (101 song name.mp3)

    p1_album = re.compile(r"^\d\d\d\d\s?[a-zA-z\s!'’&.()+~,üäáçăóéűęţ0-9\-]*$")                # 2002 name of album
    p2_album = re.compile(r"^[a-zA-zä\s!'&.,()\-]*[\d]?[\d]?[()]?$")                           # name of album
    p3_album = re.compile(r"^[a-zA-z\s!'&]*[,]\s\d\d\d\d$")                                    # name of album, 2002
        
    def print_all_regex_song_match(self, root:str) -> None:
        """ prints all audio files with particular regex pattern """

        for artist_folder in os.listdir(os.path.join(root)):
            for album_folder in os.listdir(os.path.join(root, artist_folder)):
                for file in os.listdir(os.path.join(root, artist_folder, album_folder)):
                    if file.endswith(tuple(RegexMatcher.ext)):
                        file = os.path.splitext(file)[0]
                        if RegexMatcher.p1_song.match(file): print(f"{file} -> p1_song match") 
                        elif RegexMatcher.p2_song.match(file): print(f"{file} -> p2_song match") 
                        elif RegexMatcher.p3_song.match(file): print(f"{file} -> p3_song match")
                        elif RegexMatcher.p4_song.match(file): print(f"{file} -> p4_song match")
                        else: print(f"{file} -> no regex match")


    def print_no_regex_song_match(self, root:str) -> None:
        """ prints audio files that did not match any regex pattern """

        for artist_folder in os.listdir(os.path.join(root)):
            for album_folder in os.listdir(os.path.join(root, artist_folder)):
                for file in os.listdir(os.path.join(root, artist_folder, album_folder)):
                    if file.endswith(tuple(RegexMatcher.ext)):
                        file = os.path.splitext(file)[0]
                        if RegexMatcher.p1_song.match(file):      continue
                        elif RegexMatcher.p2_song.match(file):    continue
                        elif RegexMatcher.p3_song.match(file):    continue
                        elif RegexMatcher.p4_song.match(file):    continue
                        else: print(f"{file} :: path {os.path.join(artist_folder, album_folder)} -> no regex match")


    def print_all_regex_album_match(self, root:str) -> None:
        """ print regex match pattern for all albums """ 

        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                if RegexMatcher.p1_album.match(album): print(album, " -> p1_album match")
                elif RegexMatcher.p2_album.match(album): print(album, " -> p2_album match")
                elif RegexMatcher.p3_album.match(album): print(album, " -> p3_album match")
                else: print(album, " -> no match")


    def print_no_regex_album_match(self, root:str) -> None:
        """ print albums that did not match any regex pattern """

        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                if RegexMatcher.p1_album.match(album): continue
                elif RegexMatcher.p2_album.match(album): continue
                elif RegexMatcher.p3_album.match(album): continue
                else: print(f"{album} :: path {os.path.join(root, artist)} -> no regex match")

class HelperInfo:
        
    def count_albums(root:str) -> int:
        """ return number of albums i a root dir """

        c = 0
        for artist_folder in os.listdir(root):
            for album_folder in os.listdir(os.path.join(root, artist_folder)):
                c += 1
        return c


    def print_dir_tree(root:str) -> None:
        """ prints directory tree of all files """

        for artist in os.listdir(root):
            print(artist)
            for album in os.listdir(os.path.join(root, artist)):
                print("  ", album)
                for file in os.listdir(os.path.join(root, artist, album)):
                    print("     ", file)


    def print_all_artists(root:str) -> None:
        """ prints all artist folder names - it is helper function - just to see them for further processing """

        for artist in os.listdir(root):
            print(artist)


    def print_all_albums(root:str) -> None:
        """ prints all album folder names - it is helper function - just to see them for further processing """

        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                print(album)


    def print_all_songs(root:str) -> None:
        """ prints all song folder names - it is helper function - just to see them for further processing """

        ext = get_all_audio_extensions()

        for path, dirs, folders in os.walk(root):
            for file in folders:
                if file.endswith(tuple(ext)):
                    print(file)

class BroadcastRenamer:
    pass

