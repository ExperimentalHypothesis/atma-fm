# prerequisites:
# 1] install ffmpeg and add to path
# 2] install ffmpeg-normalize [pip install ..]

# this script figures out which files are not properly ripped to minimal bitrate, based on that, it will skip normalization for those files
# files that have higher bitrate are normalized and their copy (the normalized one) is put into separate directory tree that mirrors the source one - but the root dir has extension [bitnorm]

# TODO commandline argumenty 

import os, subprocess

def check_bitrate(root: str, min_bitrate: bytes) -> dict:
  """ make a map of files having less bitrate than specified """

  audio_extensions = os.path.join(os.path.dirname(__file__), "audio_extensions.txt")
  with open(audio_extensions) as f:
      e = f.read().splitlines()
  command = "ffprobe -v error -show_entries format=bit_rate -of default=noprint_wrappers=1:nokey=1"
  d = {}
  for path, dirs, files in os.walk(root):
      for file in files:
          if file.endswith(tuple(e)):
              file_name = os.path.join(path, file)
              full_command = "".join(command + f' "{file_name}"')
              out = subprocess.check_output(full_command)
              if out < min_bitrate:
                   d[file_name] = out
  return d


def change_bitrate(source_dir: str) -> None:
  """change bitrate to defined value"""

  codec = " [lame]"
  path_replacement = "3] to be transfered"
  head, tail = os.path.split(source_dir)

  for path, dirs, files in os.walk(source_dir):
    for file in files:
      filepath_source = os.path.abspath(os.path.join(path, file))
      index = filepath_source.rfind(".") #DEBUG
      filepath_norm = filepath_source[:index] + codec + filepath_source[index:] #DEBUG
      filepath_target = filepath_norm.replace(tail, path_replacement)
      if not file.endswith(".mp3"):
        filename, extension = os.path.splitext(filepath_target)
        filepath_target = filename + ".mp3"
      dir_name = os.path.dirname(filepath_target)
      if os.path.exists(filepath_target):
        print(f"file {filepath_target} already exists, skipping..")
      else:
        if not os.path.exists(dir_name): 
          os.makedirs(dir_name)
        print(f"encoding from {filepath_source} to {filepath_target}")
        subprocess.run(f'ffmpeg -i "{filepath_source}" -metadata comment="ripped with lame @128k" -codec:a libmp3lame -b:a 128k -ar 44100 "{filepath_target}"')







if __name__ == "__main__":

  # source = r"\\192.168.0.109\lukas\online radio resources\audio - tohle se testuje pro normalizaci"
  # normalize_audio(source)

  m = check_bitrate(r"Y:\ambient\testing folder", b'160000')
  for k,v in m.items():
    print(k, v)

  # change_bitrate(r"Y:\ambient\testing folder")