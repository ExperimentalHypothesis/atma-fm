import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud
from PIL import Image

from genres_dict import genres


path_to_mask = r"C:\Users\nirvikalpa\Disk Google\coding\Python\repos\radio\app\static\img\wave.jpg"

def generate_cloud(genres: dict, path_to_mask: str):
  """ function for generating cloudword at the main page """

  mask = np.array(Image.open(path_to_mask))
  wc = WordCloud(prefer_horizontal=0.6, color_func=lambda *args, **kwargs:"white", mask=mask).generate_from_frequencies(genres)
  plt.figure(figsize=(44.88,16.88)) # hardcoded based on mask size resolution
  plt.imshow(wc)
  plt.axis("off")
  plt.tight_layout(pad=0)
  # plt.show()
  plt.savefig(r"C:\Users\nirvikalpa\Disk Google\coding\Python\repos\radio\app\static\img\logo.png")

generate_cloud(genres, path_to_mask)
