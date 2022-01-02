import os
from typing import List
from flask_restful import Resource
from application import api
from marshmallow import fields, Schema
from paramiko import channel

from application.resources.playlist import Playlist

class Albums(Resource):
    """
    GET endpoint looking like this:
        - api/albums/<artist_name> => return all albums from particular artist with channel where they are played
    """
    CHANNEL_1 = r"/audio/channel1"
    CHANNEL_2 = r"/audio/channel2"
    
    
    def get(self, artist):
        val = {}
        
        val[self.CHANNEL_1] = self.getAlbums(artist, self.CHANNEL_1)
        val[self.CHANNEL_2] = self.getAlbums(artist, self.CHANNEL_2)
        
        return {artist: val}, 200
        

    def getAlbums(self, artist: str, channel: str) -> List:
        for i in os.listdir(channel):
            if artist == i:
                return [i for i in os.listdir(os.path.join(channel, artist))]
            



api.add_resource(Albums, "/albums/<artist>")
