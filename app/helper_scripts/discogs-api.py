import discogs_client, os, pprint
from collections import namedtuple

def get_releases_from_local_filesystem(source:str) -> list:
    """ return list of releases from filesystem 
        the format of namedtuple(artist, album, [songs]) """

    Release = namedtuple("Release", ["author", "album", "songs"])
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
                    releases.append(composer)
                    releases.append(album) 
                    album_path = os.path.join(composer_path, album)
                    for song in os.listdir(album_path):
                        if os.path.isfile(os.path.join(album_path, song)) and song.endswith(tuple(e)):
                            songs.append(song)
                r = Release(composer, album, songs)
                discographies.append(r)
    return(discographies)


def get_release_versions_from_discogs_api(release_name:str) -> list: 
    """ return list of all versions of a particular release specified in argument
        the format is a namedtuple(artist, album, [songs]) """

    Release = namedtuple("API_Release", ["api_artist", "api_album", "api_songs"])
    releases = []
    
    try:
        d = discogs_client.Client('atma-fm', user_token="XqVXtxTvsRtYoPaxmvqIfBXHKxyZEqlTVYVzvDPe")
        versions = d.search(release_name, type='release')
    except Exception as e:
        print("error when connection to API", e)
    else:
        for version in versions:
            songs = []
            for track in version.tracklist:
                songs.append(track.title)
                r = Release(version.artists[0].name,version.title, songs) 
            releases.append(r)
        return releases





if __name__ == "__main__":
    root="/run/media/lukas/MULTIMEDIA"

    api_releases = get_release_versions_from_discogs_api("AaΔzhyd China Doll")
    local_releases = get_releases_from_local_filesystem()
    
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(api_releases)