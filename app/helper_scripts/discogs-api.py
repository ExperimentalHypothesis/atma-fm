import discogs_client, os, pprint, difflib
from collections import namedtuple

def get_releases_from_local_filesystem(source:str) -> list:
    """ return list of releases from filesystem 
        the format of namedtuple(artist, album, [songs]) """

    Release = namedtuple("Local_Release", ["artist", "album", "songs"])
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
                    for song in os.listdir(album_path):
                        if os.path.isfile(os.path.join(album_path, song)) and song.endswith(tuple(e)):
                            song = " ".join(song.replace("-"," ").split()[1:])
                            song = song.split(".")[0].strip(" ")
                            songs.append(song.title())
                r = Release(comp, alb, songs)
                discographies.append(r)
    return(discographies)


    # def get_release_versions_from_discogs_api(release_name:str) -> list: 
    #     """ return list of all versions of a particular release specified in argument
    #         the format is a namedtuple(artist, album, [songs]) """

    #     Release = namedtuple("API_Release", ["api_artist", "api_album", "api_songs"])
    #     releases = []
        
    #     try:
    #         d = discogs_client.Client('atma-fm', user_token="XqVXtxTvsRtYoPaxmvqIfBXHKxyZEqlTVYVzvDPe")
    #         versions = d.search(release_name, type='release')
    #     except Exception as e:
    #         print("error when connection to API", e)
    #     else:
    #         for version in versions:
    #             songs = []
    #             for track in version.tracklist:
    #                 songs.append(track.title)
    #                 r = Release(version.artists[0].name,version.title, songs) 
    #             releases.append(r)
    #         return releases

def validate_string_similarity(a:str, b:str) -> bool:
    threshold = difflib.SequenceMatcher(None, a, b).ratio()
    return True if threshold > 0.95 else False

def check_if_releases_equal(local_release: namedtuple, api_release: namedtuple, index:int) -> bool:
    """ check if release on filesystem is the same as release on discogs """

    local_tracklist = set(local_release.songs)
    api_tracklist = set(api_release.songs)

    # kdyz nejsou stejny delky, urcite nejsou stejny traklisty
    if len(local_tracklist) != len(api_tracklist):
        print(f"NO MATCH: {index}. api version has different tracklist length")
        return False
    # kdyz jsou stejny delky, udelej test setu
    elif local_tracklist == api_tracklist:
        print(f"MATCH: {index}. api version equal to local version (set comparision)")
        return True
    # kdyz jsou stejny delky ale nevysel test setu, je mozny ze je tam preklep.. udelej hlubsi test one-by-one
    else:
        for i, j in zip(sorted(local_release.songs), sorted(api_release.songs)):
            if validate_string_similarity(i, j): 
                continue
            else:
                break
        else:
            print(f"MATCH: {index}. api version equal to local version (one-by-one comparision)")
            return True
    print(f"NO MATCH: {index}. api has the same tracklist length, but the song names are different")
    return False


def get_release_versions_from_discogs_api_new(local_release:namedtuple) -> list:
    """ find the release verison on discogs that match the version on filesystem and tags it """

    local_artist, local_album, local_tracklist = local_release.artist, local_release.album, local_release.songs
    print(f"Searching for Album: {local_album} from {local_artist}")
    API_Release = namedtuple("API_Release", ["artist", "album", "songs"])
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
                if local_album == release.title:
                    print(f"Album: {local_album} from {local_artist} found! Looking up all its versions..")
                    
                    # make the list of all the versions
                    for version in release.versions:
                        songs = []
                        for track in version.tracklist:
                            songs.append(track.title)
                            api_release = API_Release(local_artist, release.title, songs)
                        versions.append(api_release)
                    print(f"{len(versions)} versions of {release.title} from {local_artist} found:")

                    # print each version
                    for index, api_release in enumerate(versions, 1):
                        print(f"\n{index}. version: {api_release}")
                    
                    # check agains local version
                    print(f"\nChecking for a match with: {local_release}\n")
                    for index, api_release in enumerate(versions, 1):
                        is_equal = check_if_releases_equal(local_release, api_release, index)
                        if is_equal:
                            print(f"API MATCH FOUND: {local_release} and {api_release} are equal.. -> skiping to another album\n")
                            break
                    else:
                        print(f"NO API MATCH FOUND for: {local_release}")
                    break
            else:
                print(f"Album {local_album} from {local_artist} NOT FOUND ON DISCOGS")
        # return versions


if __name__ == "__main__":
    root="/home/lukas/Music"
    local_releases = get_releases_from_local_filesystem(root)


    for i in local_releases:
        get_release_versions_from_discogs_api_new(i)
        print("------------------------------------------")
        # print(i)

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(api_releases)

