import discogs_client, os, pprint
from collections import namedtuple

def get_releases_from_local_filesystem(source:str) -> list:
    """ return list of releases from filesystem 
        the format of namedtuple(artist, album, [songs]) """

    Release = namedtuple("Release", ["artist", "album", "songs"])
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
                    comp = composer.replace("-", " ")
                    releases.append(comp)
                    alb = album.replace("-", " ")
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


def get_release_versions_from_discogs_api_new(r:namedtuple) -> list:
    local_artist, local_album, local_tracklist = r.artist.title(), r.album.title(), r.songs
    print(f"Searching for Album: {local_album} from {local_artist}")
    Release = namedtuple("API_Release", ["api_artist", "api_album", "api_songs"])
    versions = [] 
    try:
        d = discogs_client.Client('atma-fm', user_token="XqVXtxTvsRtYoPaxmvqIfBXHKxyZEqlTVYVzvDPe")
        releases = d.search(local_artist, type='artist')[0].releases
    except IndexError:
        print(f"Artist: {local_artist} not found on discogs.. skipping")
    except Exception as e:
        print("error when connection to API:", e)
    else:
        if releases:
            for release in releases:
                if local_album == release.title:
                    print(f"Album: {local_album} from {local_artist} found! Looking up all its versions..")
                    for version in release.versions:
                        songs = []
                        for track in version.tracklist:
                            songs.append(track.title)
                            r = Release(local_artist, release.title, songs)
                        versions.append(r)
                    break        
                else:
                    continue
            # else:
            #     print(f"NOT FOUND: {local_album} from {local_artist}" )
        return versions

if __name__ == "__main__":
    root="/home/lukas/Music"
    local_releases = get_releases_from_local_filesystem(root)

    for i in local_releases:
        versions = get_release_versions_from_discogs_api_new(i)
        print(versions)

    # api_releases = get_release_versions_from_discogs_api_new(local_releases[0])

    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(api_releases)

