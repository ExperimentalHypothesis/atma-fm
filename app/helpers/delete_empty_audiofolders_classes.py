import os, shutil


#TODO mozna to prepsat do jedny funkce.. 
class Deleter():
    """ class deleting empty audiofolders """

    def count_audiofiles(self, directory: str) -> int:
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

    #ISSUE RECURSION EROR
    def delete_folders_without_audio(self, directory: str) -> int:
        """ delete folders where no audio files are left """
        counter = 0
        for path, dirs, _ in os.walk(directory):
            if len(dirs) == 0 and self.count_audiofiles(path) == 0:
                counter += 1
                print(f"deleting.. {path}")
                shutil.rmtree(path)
                print(path)
                print(directory)
            if path != directory:
                return self.delete_folders_without_audio(directory)

    # def __call__(self):
    #     while delete_folders_without_audio(directory) != 0: 
    #         delete_folders_without_audio(director)
