import discogs_client, os, pprint, difflib, shutil
from collections import namedtuple

def get_releases_from_local_filesystem(source:str) -> list:
    """ return list of releases from filesystem 
    the format of namedtuple(artist, album, [songs], path) """

    Release = namedtuple("Local_Release", ["artist", "album", "songs", "path"])
    discographies = []

    audio_extensions = os.path.join(os.path.dirname(__file__), "audio_extensions.txt")
    with open(audio_extensions) as f:
        e = f.read().splitlines()

    for composer in os.listdir(source):
        if os.path.isdir(os.path.join(source, composer)):
            composer_path = os.path.join(source, composer)
            os.chdir(composer_path)
            for album in os.listdir(composer_path):
                releases = []
                songs = []
                if os.path.isdir(os.path.join(composer_path, album)):
                    comp = composer.replace("-", " ").title()
                    releases.append(comp)
                    alb = album.replace("-", " ").title()
                    releases.append(alb) 
                    album_path = os.path.join(composer_path, album)
                    api_path = os.path.dirname(album_path)
                    for song in os.listdir(album_path):
                        if os.path.isfile(os.path.join(album_path, song)) and song.endswith(tuple(e)):
                            song = " ".join(song.replace("-"," ").split()[1:])
                            song = song.split(".")[0].strip(" ")
                            songs.append(song.title())
                r = Release(comp, alb, songs, album_path)
                discographies.append(r)
    return(discographies)

def validate_string_similarity(a:str, b:str) -> bool:
    threshold = difflib.SequenceMatcher(None, a, b).ratio()
    return True if threshold > 0.85 else False

def check_if_releases_equal(local_release: namedtuple, api_release: namedtuple, index:int) -> bool:
    """ check if release on filesystem is the same as release on discogs """

    # local_tracklist = set(local_release.songs)
    # api_tracklist = set(api_release.songs)
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

def tag_and_move_matched_folders(source_dir:str, id:int) -> None:
    """ move folders [album version] were matched with discogs api """

    for file in os.listdir(source_dir):
        src_filepath = os.path.join(source_dir, file)
        # print(src_filepath)
        dst_filepath = src_filepath.replace("api-to_be_checked", "api-already_checked") 
        dst_filepath = os.path.join(os.path.dirname(dst_filepath) + f' [api match {id}]', file)
        if not os.path.exists(os.path.dirname(dst_filepath)):
            os.makedirs(os.path.dirname(dst_filepath))
            os.rename(src_filepath, dst_filepath)
        else:
            os.rename(src_filepath, dst_filepath)

def get_release_versions_from_discogs_api_new(local_release:namedtuple) -> None:
        """ find the release version on discogs that match the version on filesystem, tag it and move it a separate folder """

        local_artist, local_album, local_tracklist = local_release.artist, local_release.album, local_release.songs
        print(f"Searching for Album: {local_album} from {local_artist}")
        API_Release = namedtuple("API_Release", ["artist", "album", "songs", "id"])
        versions = []
        try:
            d = discogs_client.Client('atma-fm', user_token="XqVXtxTvsRtYoPaxmvqIfBXHKxyZEqlTVYVzvDPe")
            releases = d.search(local_artist, type='artist')[0].releases
        except IndexError:
            print(f"Artist {local_artist} NOT FOUND ON DISCOGS.. skipping")
        except Exception as e:
            print("error when connection to API:", e)
        else:
            if releases:
                for release in releases:
                    if difflib.SequenceMatcher(None, local_album, release.title).ratio() > 0.95:
                        print(f"Album: {local_album} from {local_artist} found! Looking up all its versions..")                  
                        # make the list of all the versions
                        try:
                            for version in release.versions:
                                songs = []
                                for track in version.tracklist:
                                    songs.append(track.title)
                                    api_release = API_Release(local_artist, release.title, songs, version.id)
                                versions.append(api_release)
                        except AttributeError as ae:
                            print(f"Album {local_album} from {local_artist} has only one version")
                        else:
                            print(f"{len(versions)} versions of {release.title} from {local_artist} found:")
                            # print each version
                            for index, api_release in enumerate(versions, 1):
                                print(f"\n{index}. version: {api_release}")
                            # check agains local version
                            print(f"\nChecking for a match with: {local_release}\n")
                        for index, api_release in enumerate(versions, 1):
                            are_equal = check_if_releases_equal(local_release, api_release, index)
                            if are_equal:
                                print(f"\nFINAL: API MATCH FOUND: {local_release} and {api_release} are equal.. -> moving and skiping to another album\n")
                                tag_and_move_matched_folders(local_release.path, api_release.id)
                                break
                        else:
                            print(f"\nFINAL: NO API MATCH FOUND for: {local_release}")
                        break
                else:
                    print(f"Album {local_album} from {local_artist} NOT FOUND ON DISCOGS")


if __name__ == "__main__":
    root="/home/lukas/Music/api-to_be_checked"
    local_releases = get_releases_from_local_filesystem(root)


    for i in local_releases:
        get_release_versions_from_discogs_api_new(i)
        print("------------------------------------------")
        # print(i)
        # tag_and_move_matched_folders(i.path)


    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(api_releases)