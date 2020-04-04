# This module is respnsile for all types of filesystem changes. In particular it means:
#  
#  - it sorts audio folders [albums] to proper place
#  - it deletes empty audio folders 
  
import os, shutil, requests
from bs4 import BeautifulSoup


class Deleter():
    """ Class deleting empty audiofolders recursively bottom up. It uses the 'audio_extensions.txt' where all audio extensions are specified (this file was scrapped from wikipedia and is saved in the same folder as this script and in case it will be lost, the scrapping function will run to replace it) """

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
        """ Save audio extension to a file """
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
        """ Count audiofiles in a directory """
        filename = "audio_extensions.txt"
        try:
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), filename)) as f:
                extensions = set(f.read().splitlines())
        except FileNotFoundError:
            print("audio_extiensions.txt file does not exists.. trying to get one from web.. ")
            Deleter.parse_audio_extensions(Deleter.scrap_audio_formats_table())
        else:
            counter = 0
            for item in os.listdir(directory):
                if any(ext in item for ext in extensions):
                    counter += 1
                else:
                    continue
            return counter


    def delete_folders_without_audio(directory: str) -> int:
        """ Delete folders where no audio files are left, recursively from botom up """
        counter = 0
        for path, dirs, _ in os.walk(directory):
            if len(dirs) == 0 and Deleter.count_audiofiles(path) == 0:
                counter += 1
                print(f"deleting.. {path}")
                shutil.rmtree(path)
        if counter > 0:
            return Deleter.delete_folders_without_audio(directory)
        else:
            return None

# TODO DELETE DUPLICATED 
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\01 Exile.flac',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\01 Exile.mp3',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\02 One Thousand Years.flac',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\02 One Thousand Years.mp3',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\03 Fetish.flac',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\03 Fetish.mp3',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\04 Body of Light.flac',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\04 Body of Light.mp3',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\05 Pan America.flac',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\05 Pan America.mp3',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\06 Breath.flac',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\05 Pan America.flac',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\05 Pan America.mp3',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\06 Breath.flac',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\06 Breath.mp3',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\07 High Places.flac',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\07 High Places.mp3',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\08 Sand Garden.flac',
#  'Y:\\ambient\\testing folder\\Tuu\\One Thousand Years\\08 Sand Garden.mp3




class Sorter():
    """ Class for sorting audio folders in a tree structure following this pattern:
        [a/name_of_composer_starting_from_letter_a/albums...]
        [b/name_of_composer_starting_from_letter_b/albums...]
        [c/name_of_composer_starting_from_letter_c/albums...]
        etc.. """

    def sort_audiofolders(source: str, target: str) -> None:
        """ Move audio folders into correct path in alphabetical structure """
        for composer in os.listdir(source):
            os.chdir(source)
            composer_path = os.path.abspath(composer)
            os.chdir(composer_path)
            for album in os.listdir(composer_path):
                if os.path.isdir(os.path.abspath(album)):
                    album_path = os.path.abspath(album)
                    dir_path = os.path.dirname(album_path)
                    target_dir = os.path.join(target, composer[0].lower(), composer, album)
                    if os.path.exists(target_dir):
                        print(f"album '{album}' on path '{album_path}' is existing on target path, skipping..")
                        continue
                    else:
                        print(f"album '{album}' on path '{album_path}' is not existing on target path '{target_dir}', moving now.. ")
                        shutil.move(album_path, target_dir)


# def split_str_on_first_number(s:str) -> str:
#     for i, c in enumerate(s):
#         if c.isdigit(): 
#             index = i
#             break
#     res = s[:index], s[index:]
#     return " ".join(res)

# import re
# p = r"Z:\Music\downloaded from bandcamp"
# for path, dirs, folders in os.walk(p):
#     for file in folders:
#         if file.endswith("mp3"):
#             filename, ext = os.path.splitext(os.path.join(path, file))
#             tracknumber, filename = "".join(filename.lstrip(path).split()[:1]), " ".join(filename.lstrip(path).split()[1:])
#             # print(tracknumber,  " - - ", filename)
#             if bool(re.search(r'\d', filename)):
#                 new_name = split_str_on_first_number(filename)
#                 dst_name = tracknumber + ' ' + new_name + ext
#                 print(os.path.join(path, dst_name))
#                 os.rename(os.path.join(path, file), os.path.join(path, dst_name))      
# #                 print(f"renaming {os.path.join(path, file)} to {os.path.join(path, dst_name)}")     
# #                 #os.rename(os.path.join(path, file), os.path.join(path, dst_name))

# # pat = re.compile(r"(^\d\d)")

# # for path, dirs, folders in os.walk(p):
# #     for file in folders:
# #         if not pat.match(file): 
# #             print(file)
