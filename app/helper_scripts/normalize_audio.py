# prerequisites:
# 1] install ffmpeg
# 2] install ffmpeg-normalize

import os

def normalize_audiofile(path_to_file: str):
  from subprocess import check_output
  if path_to_file.endswith(".flac"):
    command = f'ffmpeg-normalize "{path_to_file}" -o "{path_to_file.strip(".flac")}.mp3" -c:a mp3 -b:a 192k'
    check_output(command, shell=True)
  # elif path_to_file.endswith(".mp3"):
  #   command = f'ffmpeg-normalize "{path_to_file}" -o "{path_to_file}" -c:a mp3 -b:a 192k'
  #   check_output(command, shell=True)



def normalize_audioalbum(path_to_dir: str):
  #extension = ('.mp3', '.flac')
  for path, dirs, files in os.walk(path_to_dir):
    for file in files:
      if not file.endswith(".flac"):
        continue
      else:
        normalize_audiofile(os.path.abspath(os.path.join(path, file)))


path_to_music_dir = r"C:\Users\nirvikalpa\Music"
normalize_audiofile(path_to_music_dir)



