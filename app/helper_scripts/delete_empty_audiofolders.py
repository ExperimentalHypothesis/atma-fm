# this script will delete all folders/subfolders/subbsubfoldes (recursively from down to up) where no audiofiles are left
# it uses the audio_extensions.txt where all audio extensions are specified (this file was scrapped from wikipedia and is saved in the same folder as this script and in case it will be lost, the scrapping function will run to replace it)


import os
import shutil
import requests
from bs4 import BeautifulSoup

def scrap_audio_formats_table() -> list:
    """ scrap the table form wiki containing audioformat details """
    data = []
    try:
        website = requests.get("https://en.wikipedia.org/wiki/Audio_file_format").text
    except Exception as e:
        print("We are offline: ", e)
    else:
        soap = BeautifulSoup(website, "html.parser")
        table_body = soap.find("tbody")
        rows = table_body.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            cols_textonly = [i.text.strip() for i in cols]
            if cols_textonly:
                data.append(cols_textonly)
        return data


def parse_audio_extensions(col: list) -> None:
    """ save audio extension to a file """

    extensions = [i[0] for i in col]
    final_list = []
    for i in extensions:
        if " " not in i: 
            final_list.append(i)
        else:
            temp = i.split(", ")
            for i in temp:
                final_list.append(i)
    app_dir = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    print("succesfully made up audio_extensions.txt file\nplease rerun the script")
    with open(r"audio_extensions.txt", "w") as f:
        for i in final_list:
            print(i, file=f)
    os.chdir(app_dir)


def count_audiofiles(directory: str) -> int:
    """ count audiofiles in a directory """

    filename = "audio_extensions.txt"
    try:
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)) as f:
            extensions = set(f.read().splitlines())
    except FileNotFoundError:
        print("audio_extiensions.txt file does not exists.. trying to get one from web.. ")
        parse_audio_extensions(scrap_audio_formats_table())
    else:
        counter = 0
        for item in os.listdir(directory):
            if any(ext in item for ext in extensions):
                counter += 1
            else:
                continue
        return counter


def delete_folders_without_audio(directory: str) -> int:
    """ delete folders where no audio files are left """

    counter = 0
    for path, dirs, _ in os.walk(directory):
        if len(dirs) == 0 and count_audiofiles(path) == 0:
            counter += 1
            print(f"deleting.. {path}")
            shutil.rmtree(path)
    return counter


if __name__ == "__main__":
    source = r"\\192.168.0.109\Public\Music\slsk\!TAGGED"

    if not os.path.exists(source):
        print("directory doesnt exists, check the path")

    # delete recursively bottom up
    while delete_folders_without_audio(source) != 0:
        delete_folders_without_audio(source)
