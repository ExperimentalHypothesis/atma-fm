import discogs_client, os, pprint
#TODO

#https://www.discogs.com/oauth/authorize?oauth_token=nFcaxTtkEsPlEiIpLKqDsSSxfnWaHyjsspxUjDSS





# tohle projede rekurzivne filesystem
root="/run/media/lukas/MULTIMEDIA"
from collections import namedtuple
Release = namedtuple("Release", ["author", "album", "songs"])
discographies = []
for composer in os.listdir(root):
    if os.path.isdir(os.path.join(root, composer)):
        composer_path = os.path.join(root, composer)
        os.chdir(composer_path)
        for album in os.listdir(composer_path):
            releases = []
            songs = []
            if os.path.isdir(os.path.join(composer_path, album)):
                #print(album)
                releases.append(composer)
                releases.append(album) 
                album_path = os.path.join(composer_path, album)
                for song in os.listdir(album_path):
                    if os.path.isfile(os.path.join(album_path, song)):
                        #print(song)
                        songs.append(song)
                r = Release(composer, album, songs)
           # releases.append(songs)
            discographies.append(r)

                       

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(discographies)