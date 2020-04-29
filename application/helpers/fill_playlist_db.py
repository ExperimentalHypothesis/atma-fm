# This script fills up database with songs to be broadcasted. 
# It uses sqlalchemy, NOT flask-sqlalchemy and it is NOT part of the app
# It will be run each time i update the filesystem with new files to play


from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

Base = declarative_base()

# initialize the necessery objects
engine = create_engine("sqlite:///playlist.db", echo=False)
meta = MetaData()

# 1] initialize the table using sqlachemy syntax
songs = Table(
    'songs', meta,
    Column("id", Integer, primary_key=True),
    Column("title", String(128)),
    Column("artist", String(128)),
    Column("album", String(128)),
    Column("path", String(128))
)

meta.create_all(engine)


# # 2] initializing table using class
# class Song(Base):
#     __tablename__ = 'songs'

#     id = Column(Integer, primary_key=True)
#     title = Column(String(128))
#     artist = Column(String(128))
#     album = Column(String(128))
#     path = Column(String(128))

# Base.metadata.create_all(engine)

def parse_playlist_record(s):
    try:
        splitted = s.split("/")
        artist = splitted[4]
        album = splitted[5]
        title = splitted[6].strip(" [lame].mp3").split(" -- ")[-1]
        path = s
        return title, album, artist, path
    except IndexError:
        # dopsat kdy to ma jinej string format..
        # viz no

no = "/home/audio/bitnormed/Genesonics/14 Genesonics -- TRANSE (Changement, Volonte) -- Transe 1 [lame].mp3"

parse_playlist_record(no)


# with open("playlist.m3u", encoding="utf-8") as log:
#     with engine.connect() as conn:
#         for line in log:
#             # print(parse_playlist_record(line))
#             try:
#                 title, album, artist, path = parse_playlist_record(line)
#                 q = songs.insert().values(artist=artist, album=album, title=title, path=path)
#                 conn.execute(q)
#             except Exception as e:
#                 print(e, line)

# print(engine.table_names())

# conn = engine.connect()
# q = songs.insert().values(artist="xxx")
# conn.execute(q)
