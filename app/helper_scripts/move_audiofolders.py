# this script sorts audio folders in a tree structure like this:
# [a/name_of_composer_starting_from_letter_a/albums...]
# [b/name_of_composer_starting_from_letter_b/albums...]
# [c/name_of_composer_starting_from_letter_c/albums...]
# etc..

# $if2(%albumartist%,%artist%)/
# $if(%albumartist%,%album%/,)
# $if($gt(%totaldiscs%,1),%discnumber%-,)$if($and(%albumartist%,%tracknumber%),$num(%tracknumber%,2) ,)$if(%_multiartist%,%artist% - ,) %artist% -- %album% -- %title%

import os, shutil, delete_empty_audiofolders, time

def sort_audiofolders(source: str, target: str) -> None:
    """ move audio folders into correct path in alphabetical structure """

    for composer in os.listdir(source):
        os.chdir(source)
        composer_path = os.path.abspath(composer)
        os.chdir(composer_path)
        for album in os.listdir(composer_path):
            if os.path.isdir(os.path.abspath(album)):
                album_path = os.path.abspath(album)
                dir_path = os.path.dirname(album_path)
                #print(album_path," -- ", dir_path, " -- ", album)
                target_dir = os.path.join(target, composer[0].lower(), composer, album)
                #print(target_dir)
                if os.path.exists(target_dir):
                    print(f"album '{album}' on path '{album_path}' is existing on target path, skipping..")
                    continue
                else:
                    print(f"album '{album}' on path '{album_path}' is not existing on target path '{target_dir}', moving now.. ")
                    shutil.move(album_path, target_dir)
                    
    # TODO log how many folders were moved, how many were skipped (name which was which) 

# if __name__ == "__main__":
source = r"Z:\Music\tagged\_to be sorted"
target = r"Z:\Music\tagged"
#     try:
#         sort_audiofolders(source, target)
#     except Exception as e:
#         print(e)
# # TODO



start = time.perf_counter()
sort_audiofolders(source, target)
stop = time.perf_counter()

print(f"moving files took {stop - start} seconds")

while delete_empty_audiofolders.delete_folders_without_audio(source) != 0:
    delete_empty_audiofolders.delete_folders_without_audio(source)

