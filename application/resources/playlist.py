
from flask import request, abort
from flask_restful import Resource
from application import api
from marshmallow import Schema, fields
from application.utils.SongParser import SongParser

class Playlist(Resource):
    """
    GET endpoint that look like this:
        - api/playlist?channel=1&songs=10 => returns 10 last songs played on channel1
    """

    class PlaylistSchema(Schema):
        channel = fields.Int()
        songs = fields.Int()

    schema = PlaylistSchema()

    def get(self):
        errs = self.schema.validate(request.args)
        if errs:
            abort(400, errs)
        
        channel = int(request.args["channel"])
        songs = int(request.args["songs"])
        if channel > 2:
            abort(400, "Only 2 channels available")

        l = SongParser.getLastNSongs(songs, channel=channel)
        return {"songs": l}, 200

api.add_resource(Playlist, "/playlist")
