import os
import shutil


def count_audiofiles(directory: str) -> int:
    counter = 0
    for item in os.listdir(directory):
        if item.endswith(".mp3") or item.endswith(".flac"):
            counter += 1
        else:
            continue
    return counter


def delete_folders_without_audio(directory: str) -> int:
    counter = 0
    for path, dirs, _ in os.walk(directory):
        if len(dirs) == 0 and count_audiofiles(path) == 0:
            counter += 1
            print(f"deleting.. {path}")
            shutil.rmtree(path)
    return counter


if __name__ == "__main__":
    directory = r"\\MYCLOUDEX2ULTRA\lukas\online radio resources\audio"
    while delete_folders_without_audio(directory) != 0:
        delete_folders_without_audio(directory)
