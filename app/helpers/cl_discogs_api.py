
import discogs_client, os, pprint, difflib, shutil, re, time
from collections import namedtuple
from app.helpers.cl_audiofile_normalization import get_all_audio_extensions

print("importing cl discogs api")

api_broadcast_test =r"Y:\ambient\testing folder"
api_broadcast_test2 =r"Y:\ambient\testing folder2"
api_broadcast_test3 =r"Y:\ambient\testing folder3"



def move_nonclustered_files_to_folder(root: str) -> None:
    """ 
    when iterating over files using get_releases_from_local_filesystem() 
    there were troubles if an artist folder contained files that were not in an album subfolder.
    this function clusters there files into an 'artificial folder', thus, it should be run first to prepare the field
    """

    for artist_folder in os.listdir(root):
        for item in os.listdir(os.path.join(root, artist_folder)):
            if os.path.isfile(os.path.join(root, artist_folder, item)):
                src_path = os.path.join(root, artist_folder, item)
                dst_path = os.path.join(root, artist_folder, "artificial folder", item)
                if not os.path.exists(os.path.dirname(dst_path)):
                    os.makedirs(os.path.dirname(dst_path))
                print(f"moving {src_path} to {dst_path}")
                os.rename(src_path, dst_path)


class DiscogsApiMatcher:

    def __init__(self, source:str):
        self._source = source
        self._local_releases = [] #_local_releases


    @property
    def source(self):
        return self._source


    @property
    def local_releases(self):
        return self._local_releases


    def get_releases_from_local_filesystem(self) -> list:
        """ Return list of releases from filesystem in the the format of namedtuple(artist, album, [songs], path) """
        move_nonclustered_files_to_folder(self.source)
        ext = get_all_audio_extensions()
        Release = namedtuple("Local_Release", ["artist", "album", "songs", "path"])


        for composer in os.listdir(self.source):
            if os.path.isdir(os.path.join(self.source, composer)):
                composer_path = os.path.join(self.source, composer)
                for album in os.listdir(composer_path):
                    releases = []
                    songs = []
                    if os.path.isdir(os.path.join(composer_path, album)):
                        comp = composer.replace("-", " ").title()
                        releases.append(comp)
                        alb = album.replace("-", " ").title()
                        alb = re.sub("\d\d\d\d", "", alb).strip()
                        releases.append(alb) 
                        album_path = os.path.join(composer_path, album)
                        api_path = os.path.dirname(album_path)
                        for song in os.listdir(album_path):
                            if os.path.isfile(os.path.join(album_path, song)) and song.endswith(tuple(ext)):
                                song = " ".join(song.replace("-"," ").split()[1:])
                                song = song.split(".")[0].strip(" ")
                                songs.append(song.title())
                    r = Release(comp, alb, songs, album_path)
                    self.local_releases.append(r)
        return(self.local_releases)


    @staticmethod
    def validate_string_similarity(a:str, b:str) -> bool:
        threshold = difflib.SequenceMatcher(None, a, b).ratio()
        return True if threshold > 0.85 else False


    @staticmethod
    def have_equal_tracklist_names(local_release: namedtuple, api_release: namedtuple, index:int) -> bool:
        """ check if release on filesystem is the same as release on discogs """

        if len(local_release.songs) != len(api_release.songs):
            print(f"NO MATCH: {index}. api version has different tracklist length")
            return False
        elif local_release.songs == api_release.songs:
            print(f"MATCH: {index}. api version equal to local version (set comparision)")
            return True
        else:
            for i, j in zip(sorted(local_release.songs), sorted(api_release.songs)):
                if validate_string_similarity(i, j): 
                    continue
                else:
                    break
            else:
                print(f"MATCH: {index}. api version equal to local version (one-by-one comparision)")
                return True
        print(f"NO MATCH: {index}. api version has the same tracklist length, but the song names are different")
        return False


    @staticmethod
    def tag_and_move_matched_folders(source_dir:str, directory_name:str) -> None:
        """ move folders [album version] were matched with discogs api and change path names based on this format
        
            old:
            path='Z:\\Music\\api\\api-to_be_checked\\andrew lahiff\\2009 tales of hidden algebra')

            new:
            path='Z:\\Music\\api\\1] api match [by names]\\Andrew Lahiff\\Tales Of Hidden Algebra [api match 123456]')
            path='Z:\\Music\\api\\1] api match [by names]\\<API_Release.artist>\\<API_Release.album [api match {id[0]}]>')
        """

        for file in os.listdir(source_dir):
            src_filepath = os.path.join(source_dir, file)
            dst_filepath = src_filepath.replace("api-to_be_checked", directory_name) 
            if id:
                dst_filepath = os.path.join(os.path.dirname(dst_filepath) + f' [api match {id[0]}]', file)
            else:
                dst_filepath = os.path.join(os.path.dirname(dst_filepath), file)
            if not os.path.exists(os.path.dirname(dst_filepath)):
                os.makedirs(os.path.dirname(dst_filepath))
                os.rename(src_filepath, dst_filepath)
            else:
                os.rename(src_filepath, dst_filepath)


    @staticmethod
    def match_release_versions_from_discogs_api_by_artist(local_release:namedtuple) -> None:
            """ find the release version [query by artist] match the version on filesystem tag it and move it a separate folder """

            local_artist, local_album, local_tracklist = local_release.artist, local_release.album, local_release.songs
            print(f"Searching for Album: {local_album} from {local_artist}")
            API_Release = namedtuple("API_Release", ["artist", "album", "songs", "id"])
            versions = []
            try:
                d = discogs_client.Client('atma-fm', user_token="XqVXtxTvsRtYoPaxmvqIfBXHKxyZEqlTVYVzvDPe")
                releases = d.search(local_artist, type='artist')[0].releases
                #time.sleep(1)
            except IndexError:
                print(f"Artist {local_artist} NOT FOUND ON DISCOGS.. skipping")
                tag_and_move_matched_folders(local_release.path, "5] artist not found on discogs api")
            except Exception as e:
                print("error when connection to API:", e)
            else:
                if releases:
                    for release in releases:
                        if difflib.SequenceMatcher(None, local_album, release.title).ratio() > 0.95:
                            print(f"Album: {local_album} from {local_artist} found! Looking up all its versions..")                  
                            one_release = release 
                            
                            # make the list of all the versions 
                            try:
                                for version in release.versions:
                                    songs = []
                                    for track in version.tracklist:
                                        songs.append(track.title)
                                        api_release = API_Release(local_artist, release.title, songs, version.id)
                                        time.sleep(1)
                                    versions.append(api_release)
                        
                            # make the list when it has only one version
                            except AttributeError as ae:
                                songs = []
                                for track in one_release.tracklist:
                                    songs.append(track.title)
                                api_release = API_Release(local_album, one_release.title, songs, one_release.id)
                                versions.append(api_release)
                        
                            # print the versions that you found
                            print(f"{len(versions)} versions of {release.title} from {local_artist} found:")
                            for index, api_release in enumerate(versions, 1):
                                print(f"\n{index}. version: {api_release}")
                        
                            # try to find match with an api version based on tracklist names
                            match_found = False
                            print(f"\nChecking for a match based on tracklist names with: {local_release}\n")
                            for index, api_release in enumerate(versions, 1):
                                if have_equal_tracklist_names(local_release, api_release, index):
                                    print(f"\n>> FINAL: API MATCH FOUND << on tracklist names: {local_release} and {api_release} are equaly named -> moving and skiping to another album\n")
                                    tag_and_move_matched_folders(local_release.path, "1] api match [by names]", api_release.id)
                                    match_found = True
                                    break
                            else:
                                print(f"\nNo match based on tracklist names for: {local_release}\n")
                                    
                            # if it did not find match on names, try find match with an api version based on tracklist length
                            if not match_found:
                                print(f"\n Checking for a match based on length only with: {local_release}\n")
                                for index, api_release in enumerate(versions, 1): 
                                    if len(local_release.songs) == len(api_release.songs):
                                        print(f"\n>> FINAL: API MATCH FOUND << on tracklist length: {local_release} and {api_release} are equally long -> moving and skiping to another album\n")
                                        tag_and_move_matched_folders(local_release.path, "2] api match [by length]", api_release.id)
                                        match_found = True
                                        break
                                else:
                                    print(f"\nNo match based on tracklist length for: {local_release}\n")
                        
                            # if not matched with names or length, it is probbaly incomplete..
                            if not match_found:                      
                                print(f"Album {local_release.album} from {local_release.artist} is incomplete -> moving to INCOMPLETE FOLDER")
                                tag_and_move_matched_folders(local_release.path, "3] api match [not found - incomplete tracklist]", 0)
                            
                            break # this break needs to be here in order to jump out of the for loop and not to print the statement bellow
                    else:
                        print(f"Album {local_album} from {local_artist} NOT FOUND ON DISCOGS -> moving and skiping to another album\n")
                        tag_and_move_matched_folders(local_release.path, "4] album not found on discogs api")



