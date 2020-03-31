import os, shutil


class Deleter():
    """ Class deleting empty audiofolders """

    def count_audiofiles(directory: str) -> int:
        """ Count audiofiles in a directory """
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
