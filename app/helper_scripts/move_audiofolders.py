import os, shutil

#tohl eje potreba dodelat protoze to nefunguje
def move_audiofolders(source, dest):
    from string import ascii_letters
    import distutils.dir_util
    for foder_name in os.listdir(source):
        first_token = i[0]
        for token in ascii_letters:
            if token == first_token:
                token = token.lower()
                print('moving ', os.path.join(source, i), ' to ', dest+f"\{token}" )
                distutils.dir_util.copy_tree(os.path.join(source, foder_name), os.path.join(dest+f"\{token}", folder_name))

copy_to = r"C:\Users\nirvikalpa\Desktop\novytest"
copy_from =r"C:\Users\nirvikalpa\Desktop\novytest\complete"

def move_audiofolders(src, dst):
    """ helper function for transposing folders with music """

    import shutil
    for composer in os.listdir(src):
        os.chdir(src)
        composer_path = os.path.abspath(composer)
        os.chdir(composer_path)
        for album in os.listdir(composer_path):
            if os.path.isdir(os.path.abspath(album)):
                album_path = os.path.abspath(album)
                album_name = os.path.basename(album_path)
                source_dir = os.path.abspath(album_path)
                target_dir = dst + '\\'+ composer[0].lower() + '\\' + composer + "\\" + album # tohle prepsat joi
                print("moving..", source_dir)
                print("to.. ", target_dir)

                if os.path.exists(target_dir):
                    print(source_dir, " already exist..")
                    continue
                else:
                    shutil.move(source_dir, target_dir)
                    print(os.getcwd())



# if name == main


# source = r"\\192.168.0.109\Public\Music\slsk\!TAGGED"
# dest = r"\\192.168.0.109\Public\Music"
# move_audiofolders(source, dest)