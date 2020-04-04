import bandcamp_dl, os, subprocess, requests, pathlib
from bs4 import BeautifulSoup
from importlib import reload

from app.helpers.cl_audiofile_normalization import NameNormalizer

# reload(cl_audiofile_normalization)

class BandcampScrapper:
    """ Class for scrapping data from Bandcamp. It scraps genres, downloads albums and renames the downloaded files."""

    def __init__(self, name:str, base_dir:str ="Z:\\Music\\from bandcamp") -> None:
        """ name has to passed as one string eg: steveroach, not steve-roach, or steve roach etc.."""
        self._name = name
        self._base_dir = base_dir
        self.author_albums = set()
        # self.other_albums = set()        # tohle je tady na co ?

        self.author_album_urls = set()
        self.label_albums_urls = set()


    def __repr__(self):
        return f"BandcampScrapper(name='{self.name}', base_dir='{self._base_dir}')"
        

    @property
    def name(self):
        return self._name


    @property
    def base_dir(self):
        return self._base_dir


    @property
    def base_url(self):
        return f"http://www.{self.name}.bandcamp.com" 


    def prepare_dl_links(self) -> list:
        """ Prepare links of all full albums only from the specified [base_url] """
        try:
            website = requests.get(self.base_url).text
        except Exception as e:
            print("we are offline\n", e)
        else:
            soup = BeautifulSoup(website, "html.parser")
            for a in soup.find_all("a", href=True):
                if "/album/" in a["href"] and "http" in a["href"]: 
                    self.label_albums_urls.add(a["href"])
                elif "/album/" in a["href"]: 
                    self.author_albums.add(a["href"])
            for album in self.author_albums:
                self.author_album_urls.add(self.base_url + album)
                # self.author_album_urls.extend(self.other_albums)      # tohle je tady na co ?


    def dl_author_albums(self) -> None:
        """ Download albums attached to author""" 
        for url in self.author_album_urls:
            subprocess.run(f'bandcamp-dl {url} -f --base-dir="{self._base_dir}"')


    def dl_label_albums(self) -> None:
        """ Download albums attached to label""" 
        for url in self.label_albums_urls:
            subprocess.run(f'bandcamp-dl {url} -f --base-dir="{self._base_dir}"')


    def normalize_names(self) -> None:
        """ Normalize names of artist, albums, songs that were just downloaded """
        NameNormalizer.titlecase_all(self.base_dir)
        NameNormalizer.strip_dash_from_artist_album_song(self.base_dir)


     def scrap_genres(url:str) -> None
        """ Scrap genres from particular author or label """

        scrapped_tags = set()
        try:
            website = requests.get(url).text
        except Exception as e:
            print(e)
        else:
            soup = BeautifulSoup(website, "html.parser")
            for tag in soup.find_all("a", {"class": "tag"}):
                scrapped_tags.add(tag.text.lower())
        genres_txt = pathlib.Path().absolute().joinpath('app', 'helpers', 'genres.txt')
        with open(genres_txt, "r+") as f:
            infile_tags = set(f.read().splitlines())
            tags_to_add = scrapped_tags - infile_tags
            for tag in tags_to_add:
                f.write(str(tag) + "\n")
           






if __name__ == "__main__":
   pass
