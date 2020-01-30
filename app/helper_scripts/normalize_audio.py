# prerequisites:
# 1] install ffmpeg and add to path
# 2] install ffmpeg-normalize [pip install ..]

import os, subprocess

def check_bitrate(root: str, min_bitrate: bytes) -> dict:
  """ make a map of files having less bitrate than specified """

  with open(r"C:\Users\lukas\source\repos\python\online-radio\app\helper_scripts\audio_extensions.txt") as f:
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


#TODO udelat aby to bralo commandline argumenty jako cesty odkud kam
def normalize_audio(source: str) -> None:
  with open(r"C:\Users\lukas\source\repos\python\online-radio\app\helper_scripts\audio_extensions.txt") as f:
    exts = f.read().splitlines()
  norma = " [peak norm -5]"
  #ffmpeg_command = f'ffmpeg-normalize "{filepath_old}" -o "{filepath_new}" -c:a mp3 -ar 44100'

  for path, _, files in os.walk(source):
      for file in files:
          if file.endswith(".mp3"):
              filepath_source = os.path.join(path, file)
              index = filepath_source.rfind(".")
              filepath_norm = filepath_source[:index] + norma + filepath_source[index:]
              filepath_target = filepath_norm.replace("audio", "normalized test") #TODO tadyto prepsat aby to bylo univerzalnejsi pri commandline argumentech
              head, _ = os.path.split(filepath_target)
              if os.path.exists(head):
                  print(f'normalizing "{filepath_source}" saving to "{filepath_target}" ')
                  subprocess.run(f'ffmpeg-normalize "{filepath_source}" -nt peak -t -5 -o "{filepath_target}" -c:a libvorbis -ar 44100')
              else:
                  os.makedirs(head)
                  print(f'normalizing "{filepath_source}" saving to "{filepath_target}" ')
                  subprocess.run(f'ffmpeg-normalize "{filepath_source}" -nt peak -t -5 -o "{filepath_target}" -c:a libvorbis -ar 44100')


if __name__ == "__main__":
  source = r"\\192.168.0.109\lukas\online radio resources\audio - tohle se testuje pro normalizaci"
  normalize_audio(source)
