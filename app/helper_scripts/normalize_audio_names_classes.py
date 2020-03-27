import os, re, mutagen, shutil, pathlib
from collections import namedtuple

print("importing..")

api_match_testing = r"Z:\Music\api\t\2] api match [by length]"
api_notfound = r"Z:\Music\api\4] album not found on discogs api"


def get_all_audio_extensions() -> list:
    """ returns audio extensions specified in file. must be called from root of the project. works both for shell and non shell, win i linux """
    audio_extensions = pathlib.Path().absolute().joinpath('app', 'helper_scripts','audio_extensions.txt')  
    with open(audio_extensions) as f:
        ext = f.read().splitlines()
    return ext


def move_albums_with_one_track_only(root:str) -> None:
    """ moves albums with one track to separate folder """
    singletrack_albums = []
    ext = get_all_audio_extensions()
    one_only = "_ALBUMS_WITH_ONE_TRACK_"

    for artist in os.listdir(root):
        for album in os.listdir(os.path.join(root, artist)):
            tracklist = [track for track in os.listdir(os.path.join(root, artist, album)) if track.endswith(tuple(ext))]
            if len(tracklist) == 1:
                print(f"Album '{album}' on path {os.path.join(root, artist)} has only one track")
                singletrack_albums.append(album)
                for track in tracklist:
                    src_file = os.path.join(root, artist, album, track)
                    root_one_only = root + one_only
                    dst_file = os.path.join(root_one_only, artist, album, track)
                    if not os.path.exists(os.path.dirname(dst_file)):
                        os.makedirs(os.path.join(root_one_only, artist, album))
                    print(f"Moving {src_file} to {dst_file}")
                    shutil.move(src_file, dst_file)
    print(f"Totaly: {len(singletrack_albums)} with one track only")


class NameNormalizer:
    """ class for clearing out the names of songs, artists and albums, the goal is to have:
        clear {artist_name} in the form of plain "artist name"          => for example "steve roach" 
        clear {album_name} in the form of plain "album name"            => for example "structures of silence"
        clear {song name} in the of "song name" with track number       => for example "01 early man.mp3"
    """ 
    def __repr__(self):
        pass


    def __call__(self, root):
        """ calls the function in appropriate order """
        NameNormalizer.strip_apimatch_from_albumname(self, root)
        NameNormalizer.strip_year_from_albumname(self, root)
        NameNormalizer.titlecase_all(self, root)
        NameNormalizer.strip_year_from_songname(self, root)
        NameNormalizer.strip_artist_album_name_from_songname(self, root)
        NameNormalizer.strip_whitespaces_from_songname(self, root)
        NameNormalizer.strip_dot_after_track_from_songname(self, root)
        NameNormalizer.strip_parens_around_track_from_songname(self, root)
        NameNormalizer.strip_whitespaces_from_songname(self, root)
    

    def strip_artist_album_name_from_songname(self, root:str) -> None:
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


    def strip_year_from_songname(self, root:str) -> None:
        """ deletes (year) and Cd and _- from song name """
        ext = get_all_audio_extensions()
        yr_parens = re.compile(r"[(]\d\d\d\d[)]")
        cd = re.compile(r"Cd\s?\d\d?")
        for path, dirs, folders in os.walk(root):
            for file in folders:
                if file.endswith(tuple(ext)):
                    if re.search(yr_parens, file) or re.search(cd, file) or "-" in file or "_" in file or "[" in file or "]" in file:
                        #print(f"stripping yr from {file}")
                        new_file_name = re.sub(yr_parens, "", file).strip()
                        #print(f"stripping cd from {file}")
                        new_file_name = re.sub(cd, "", new_file_name).strip()
                        #print(f"stripping '-' from {file}")
                        new_file_name = new_file_name.replace("-", " ").replace("_", " ").strip()
                        #print(f"stripping '_' from {file}")
                        new_file_name = new_file_name.replace("[", "").replace("]", "").strip()
                        src_file = os.path.join(path, file)
                        dst_file = os.path.join(path, new_file_name)                    
                        os.rename(src_file, dst_file)


    def strip_dash_underscores_from_songname(self, root:str) -> None:
        """ deletes _ and - from all song names """
        ext = get_all_audio_extensions()
        for path, dirs, folders in os.walk(root):
            for file in folders:
                if file.endswith(tuple(ext)) and ("-" in file or "_" in file):
                    new_file_name = file.replace("-", " ").replace("_", " ")
                    src_name = os.path.join(path, file)
                    dst_name = os.path.join(path, new_file_name)
                    print(f"Striping -_ from song name {src_name} -> {dst_name}")
                    os.rename(src_name, dst_name)

         
    def strip_whitespaces_from_songname(self, root:str) -> None:
        """ delete multiple spaces in song names, ale trailing space at the end as well """
        for path, dirs, files in os.walk(root):
            for file in files:
                if "  " in file or file[0] == " ":           
                    src_file = os.path.join(path, file)
                    file = re.sub(r"[\s]+", " ", file).strip()
                    dst_file = os.path.join(path, file)
                    print(f"Stripping whitespace from {src_file} --> {dst_file}")
                    os.rename(src_file, dst_file)                   
                path_file_without_ext, ext = os.path.splitext(os.path.join(path, file))
                if path_file_without_ext[-1] == " ":
                    new_file_name = path_file_without_ext.strip()+ext
                    src_file = os.path.join(path, file)
                    dst_file = os.path.join(path, new_file_name)
                    print(f"Stripping whitespace as last char {src_file} --> {dst_file}")
                    os.rename(src_file, dst_file)   


    def strip_dot_after_track_from_songname(self, root:str) -> None:
        """ some songs have this format: 01. songname.mp3, or 1. songname, strip the . """
        for path, dirs, files in os.walk(root):
            for file in files:
                file_name, ext = os.path.splitext(os.path.join(path, file))
                basename = os.path.basename(file_name)
                try:
                    if os.path.basename(file_name)[2] == "." or os.path.basename(file_name)[1] == ".":
                        src_file = os.path.join(path, file)
                        dst_file = os.path.join(path, file_name.replace(".","", 1)+ext)
                        print(f"Stripping dot from {file}")
                        os.rename(src_file, dst_file)
                except IndexError as e:
                    print(f"{e}, {os.path.join(path, file)} does not have song name")


    def strip_parens_around_track_from_songname(self, root:str) -> None:
        """ some songs have this format: (02) Secret Light At The Upper Window, strip the () """
        ext = get_all_audio_extensions()
        for path, dirs, folders in os.walk(root):
            for file in folders:
                if file.endswith(tuple(ext)):
                    if file[0] == "(" and file[3] == ")":
                        src_name = os.path.join(path, file)
                        dst_name = os.path.join(path, file.replace("(","", 1).replace(")","", 1))
                        print(f"Stripping parens arount songname {file}")
                        os.rename(src_name, dst_name)

    @staticmethod
    def strip_whatever_from_songname(s:set, substrings:list) -> None:
        """ used for manual clearing when we see which songs with no regex match, takes a list os strings that should be stripped out """
        for path in s:
            head, tail = os.path.split(path)
            for substring in substrings:
                if substring in tail:
                    new_tail = tail.replace(substring, "").strip()
                    dst = os.path.join(head, new_tail)
                    os.rename(path, dst)

    @staticmethod
    def split_tracknumber_from_name_in_songname(s:set) -> None:
        """ some song have this format 10songname.mp3, this will meke it 10 songname.mp3 """
        for song in s:
            head, tail = os.path.split(song)
            if tail[:2].isdigit() and (isinstance(tail[2:], str) and tail[2] != " "):
                new_tail = tail[:2] + " " + tail[2:]
                src = song
                dst = os.path.join(head, new_tail)
                print(f"Spliting tracknumber from name {tail} -> {new_tail}")
                os.rename(src, dst)            


    def strip_year_from_albumname(self, root:str) -> None:
        """ deletes year from album name """
        p1_album = re.compile(r"^[a-zA-zä\s!'&.,()\-]*[\d]?[\d]?[()]?$")                                            # name of album
        p2_album = re.compile(r"^(\d\d\d\d)(\s?)([a-zA-z\s!'’&.()+~,üäöáçăóéűęěščřžýáíţ0-9\-]*)$")                   # 2002 name of album
        p3_album = re.compile(r"^([a-zA-z\s!'&]*)([,]\s)(\d\d\d\d)$")                                               # name of album, 2002        

        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                if p2_album.match(album) or p3_album.match(album):
                    p2_match = p2_album.match(album)
                    p3_match = p3_album.match(album)
                    try:
                        album_title = p2_match.group(3)
                    except AttributeError:
                        pass
                    try:
                        album_title = p3_match.group(1)
                    except AttributeError:
                        pass
                    
                    src_name = os.path.join(root, artist, album)
                    dst_name = os.path.join(root, artist, album_title)
                    print(f"Renaming album, stripping year {album} -> {album_title}")
                    if not os.path.exists(dst_name):
                        os.rename(src_name, dst_name)
                    else:
                        print(f"Ablbum {dst_name} already exists, removing duplicates")
                        shutil.rmtree(src_name)


    def strip_apimatch_from_albumname(self, root:str) -> None:
        """ strip [api match 131243] from album folder """
        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                if "api match" in album:
                    album_name = album.rsplit(' [api')[0]
                    src_name = os.path.join(root, artist, album)
                    dst_name = os.path.join(root, artist, album_name)
                    print(f"reaming {src_name} to {dst_name}")
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


class RegexPatternsProvider:
    """ base class for SongTagger and RegexMatcher, this basically only encapulates regex patters to have them in one place """
    p1_song = re.compile(r"(^\d\d)(\s)([\w+\s().,:#=`&'?!\[\]]*)$")                                          # one CD leading zero (01 song name.mp3)
    p2_song = re.compile(r"(^\d)(\s)([A-Z][\w+\s().,:#=`&'?!\[\]]*)$")                                   # one CD no leading zero (1 song name.mp3)
    p3_song = re.compile(r"(^\d\s\d\d)(\s)([\w+\s().,:#=&`'?!\[\]]*)$")                                 # multiple CD (1 01 song name.mp3)
    p4_song = re.compile(r"(^\d\d\d)(\s)([\w+\s().,:#=&'?`!\[\]]*)$")                                   # multiple CD (101 song name.mp3)

    p1_album = re.compile(r"^[a-zA-zä\s!'&.,()\-]*[\d]?[\d]?[()]?$")                                    # name of album
    p2_album = re.compile(r"^(\d\d\d\d)(\s?)([a-zA-z\s!'’&.()+~,üäöáçăóéűęěščřžýáíţ0-9\-]*)$")          # 2002 name of album
    p3_album = re.compile(r"^([a-zA-z\s!'&]*)([,]\s)(\d\d\d\d)$")                                       # name of album, 2002


class RegexMatcher(RegexPatternsProvider):

    ext = get_all_audio_extensions()

    p1_song_matches = set() 
    p2_song_matches = set() 
    p3_song_matches = set()
    p4_song_matches = set()
    no_song_matches = set()

    p1_album_matches = set()
    p2_album_matches = set()    
    p3_album_matches = set()
    no_album_matches = set()

    def get_all_regex_song_match(self, root:str) -> None:
        """ prints all audio files with particular regex pattern """
        self.p1_song_matches.clear() 
        self.p2_song_matches.clear() 
        self.p3_song_matches.clear()
        self.p4_song_matches.clear()
        self.no_song_matches.clear()

        for artist_folder in os.listdir(os.path.join(root)):
            for album_folder in os.listdir(os.path.join(root, artist_folder)):
                for file in os.listdir(os.path.join(root, artist_folder, album_folder)):
                    if file.endswith(tuple(RegexMatcher.ext)):
                        file, ext = os.path.splitext(file)
                        if self.p1_song.match(file): 
                            print(f"{file+ext} -> p1_song match")
                            RegexMatcher.p1_song_matches.add(os.path.join(root, artist_folder, album_folder, file+ext)) 
                        elif RegexMatcher.p2_song.match(file): 
                            print(f"{file+ext} -> p2_song match")
                            RegexMatcher.p2_song_matches.add(os.path.join(root, artist_folder, album_folder, file+ext)) 
                        elif RegexMatcher.p3_song.match(file): 
                            print(f"{file+ext} -> p3_song match")
                            RegexMatcher.p3_song_matches.add(os.path.join(root, artist_folder, album_folder, file+ext))
                        elif RegexMatcher.p4_song.match(file): 
                            print(f"{file+ext} -> p4_song match")
                            RegexMatcher.p4_song_matches.add(os.path.join(root, artist_folder, album_folder, file+ext))
                        else: 
                            RegexMatcher.no_song_matches.add(os.path.join(root, artist_folder, album_folder, file+ext))
                            print(f"{file+ext}  :: path {os.path.join(artist_folder, album_folder)} -> no regex match")


    def get_no_regex_song_match(self, root:str) -> None:
        """ prints audio files that did not match any regex pattern """
        self.no_song_matches.clear()

        for artist_folder in os.listdir(os.path.join(root)):
            for album_folder in os.listdir(os.path.join(root, artist_folder)):
                for file in os.listdir(os.path.join(root, artist_folder, album_folder)):
                    if file.endswith(tuple(RegexMatcher.ext)):
                        file, ext = os.path.splitext(file)
                        if RegexMatcher.p1_song.match(file):      continue
                        elif RegexMatcher.p2_song.match(file):    continue
                        elif RegexMatcher.p3_song.match(file):    continue
                        elif RegexMatcher.p4_song.match(file):    continue
                        else: 
                            print(f"{file+ext} :: path {os.path.join(artist_folder, album_folder)} -> no regex match")
                            self.no_song_matches.add(os.path.join(root, artist_folder, album_folder, file+ext))


    def get_all_regex_album_match(self, root:str) -> None:
        """ print regex match pattern for all albums """ 
        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                if RegexMatcher.p1_album.match(album): 
                    print(album, f" -> p1_album match :: path {os.path.join(root, artist)}")
                elif RegexMatcher.p2_album.match(album): 
                    print(album, f" -> p2_album match :: path {os.path.join(root, artist)}")
                elif RegexMatcher.p3_album.match(album): 
                    print(album, f" -> p3_album match :: path {os.path.join(root, artist)}")
                else: 
                    print(album, " -> no match")


    def get_no_regex_album_match(self, root:str) -> None:
        """ print albums that did not match any regex pattern """
        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                if RegexMatcher.p1_album.match(album):      continue
                elif RegexMatcher.p2_album.match(album):    continue
                elif RegexMatcher.p3_album.match(album):    continue
                else: 
                    print(f"{album} :: path {os.path.join(root, artist)} -> no regex match")
    

    def count_albums_with_no_regex_matched_songs(self, s:set) -> int:
        """ returns number of albums whose songs did not match any regex patter and thus will not be tagged """
        uni_paths = {os.path.split(song) for song in s}
        return len(uni_paths)


    def print_albums_with_no_regex_matched_songs(self, s:set) -> int:
        """ prints the albums whose songs did not match any regex patter and thus will not be tagged """
        uni_paths = {os.path.dirname(song) for song in s}
        for i in uni_paths: 
            print(i)



#TODO dopsat deleter po presunuti
class SongTagger(RegexPatternsProvider):
    """ class that tags songs, names are parsed from filesystem, thus first they need to be normalized. after tagging, the untagged songs are move to separated folder """
    ext = get_all_audio_extensions()

    def tag_songs(self, root:str) -> None:
        """ tag songs based on regexes  """
        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                songs = [track for track in os.listdir(os.path.join(root, artist, album)) if track.endswith(tuple(SongTagger.ext))]
                paths = [os.path.join(root, artist, album, track) 
                        for track in os.listdir(os.path.join(root, artist, album)) if track.endswith(tuple(SongTagger.ext))]
                for song, path in zip(songs, paths):
                    song_name = song.rsplit(".", 1)[0].title()
                    if SongTagger.p1_song.match(song_name) or SongTagger.p2_song.match(song_name) or SongTagger.p3_song.match(song_name) or SongTagger.p4_song.match(song_name):
                        p1_match = SongTagger.p1_song.match(song_name)
                        p2_match = SongTagger.p2_song.match(song_name)
                        p3_match = SongTagger.p3_song.match(song_name)
                        p4_match = SongTagger.p4_song.match(song_name)
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
                        print(f"Song on path {path} doesnt match regex -> NOT TAGGED, moving..")
                        SongTagger.move_untagged_files(root, path)


    def move_untagged_files(root:str, path:str) -> None:
        """ moves untagged files to sepateated folder """
        untagged = "_UNTAGGED_"

        if not os.path.exists(os.path.join(root, untagged)):
            os.mkdir(os.path.join(root, untagged))
        else:            
            tail_path = path.lstrip(root)
            dst_filepath = os.path.join(root, untagged, tail_path)
            dst_directory = os.path.dirname(os.path.join(root, untagged, tail_path))
            if not os.path.exists(dst_directory):
                print(f"Creating .. {dst_directory}")
                os.makedirs(dst_directory)
            print(f"Moving untagged file from {path} to {dst_filepath}")
            shutil.move(path, dst_filepath)
    
    # def move_onetrack_albums()


class HelperInfo(RegexPatternsProvider):

    ext = get_all_audio_extensions()

    def count_albums(self, root:str) -> int:
        """ return number of albums i a root dir """
        c = 0
        for artist_folder in os.listdir(root):
            for album_folder in os.listdir(os.path.join(root, artist_folder)):
                c += 1
        return c

    def print_dir_tree(self, root:str) -> None:
        """ prints directory tree of all files """
        for artist in os.listdir(root):
            print(artist)
            for album in os.listdir(os.path.join(root, artist)):
                print("  ", album)
                for file in os.listdir(os.path.join(root, artist, album)):
                    print("     ", file)


    def print_all_artists(self, root:str) -> None:
        """ prints all artist folder names """
        for artist in os.listdir(root):
            print(artist)


    def print_all_albums(self, root:str) -> None:
        """ prints all album folder names """
        for artist in os.listdir(root):
            for album in os.listdir(os.path.join(root, artist)):
                print(album)


    def print_all_songs(self, root:str) -> None:
        """ prints all song folder names """
        for path, dirs, folders in os.walk(root):
            for file in folders:
                if file.endswith(tuple(HelperInfo.ext)):
                    print(file)




class BroadcastRenamer:
    pass



if __name__ == "__main__":
    x = get_all_audio_extensions()
    print(x)
