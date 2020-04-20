


# #TODO udelat aby to bralo commandline argumenty jako cesty odkud kam
# def normalize_audio_volume(source: str) -> None:

#   with open(r"C:\Users\lukas\source\repos\python\online-radio\app\helper_scripts\audio_extensions.txt") as f:
#     exts = f.read().splitlines()
#   norma = " [peak norm -5]"
#   #ffmpeg_command = f'ffmpeg-normalize "{filepath_old}" -o "{filepath_new}" -c:a mp3 -ar 44100'

#   for path, _, files in os.walk(source):
#       for file in files:
#           if file.endswith(".mp3"):
#               filepath_source = os.path.join(path, file)
#               index = filepath_source.rfind(".")
#               filepath_norm = filepath_source[:index] + norma + filepath_source[index:]
#               filepath_target = filepath_norm.replace("audio", "normalized test") #TODO tadyto prepsat aby to bylo univerzalnejsi pri commandline argumentech
#               head, _ = os.path.split(filepath_target)
#               if os.path.exists(head):
#                   print(f'normalizing "{filepath_source}" saving to "{filepath_target}" ')
#                   subprocess.run(f'ffmpeg-normalize "{filepath_source}" -nt peak -t -5 -o "{filepath_target}" -c:a libvorbis -ar 44100')
#               else:
#                   os.makedirs(head)
#                   print(f'normalizing "{filepath_source}" saving to "{filepath_target}" ')
#                   subprocess.run(f'ffmpeg-normalize "{filepath_source}" -nt peak -t -5 -o "{filepath_target}" -c:a libvorbis -ar 44100')