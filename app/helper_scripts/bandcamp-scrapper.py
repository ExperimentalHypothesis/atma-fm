import bandcamp_dl, os, sys
from bs4 import BeautifulSoup
import requests

def prepare_urls(name: str) -> list:
    """ make list of url that can be downloaded """

    # www.steveroach.bancamp.com/album/early-man
    base_url = f"http://www.{name}.bandcamp.com" 
    album_urls = []
    try:
        website = requests.get(base_url).text
    except Exception as e:
        print("we are offline\n", e)
    else:
        author_albums = set()
        label_albums = set()
        other_albums = set()
        soup = BeautifulSoup(website, "html.parser")
        for a in soup.find_all("a", href=True):
            if "/album/" in a["href"] and "http" in a["href"]:
                label_albums.add(a["href"])
            elif "/album/" in a["href"]:
                author_albums.add(a["href"])
        for album in author_albums:
            album_urls.append(base_url + album)
            album_urls.extend(other_albums)
        return album_urls

def download_full_albums(urls: list) -> None:
    """ download the albums specified in list of url"""

    for url in urls:
        subprocess.run(f"bandcamp-dl {url} -f")


import subprocess
if __name__ == "__main__":
    albums = prepare_urls("...")
    print(albums)
    # x = subprocess.run("bandcamp-dl https://steveroach.bandcamp.com/album/painting-in-the-dark -f")

    # download_full_albums(prepare_urls("steveroach"))
