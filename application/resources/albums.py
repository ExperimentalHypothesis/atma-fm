import os
from difflib import get_close_matches
from typing import List
from flask_restful import Resource
from application import api
from marshmallow import fields, Schema


class Albums(Resource):
    """
    GET endpoint looking like this:
        - api/albums/<artist_name> => return all albums from particular artist with channel where they are played on
    """


    def get(self, artist):
        val = {}

        val["channel1"] = self._getAlbums(artist, "/audio/channel1")
        val["channel2"] = self._getAlbums(artist, "/audio/channel2")

        return {artist: val}, 200

    def _getAlbums(self, artist: str, channel: str) -> List:
        artists = os.listdir(channel)
        for i in artists:
            if artist == i:
                return [i for i in os.listdir(os.path.join(channel, artist))]

        matches = get_close_matches(artist, artists, cutoff=0.7)

        if matches:
            matches = [i.lower() for i in matches]
            return f"{artist} not found, did you mean {matches}?"

        return f"{artist} not found"


api.add_resource(Albums, "/albums/<artist>")
