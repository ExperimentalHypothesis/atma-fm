from flask import request, abort
from flask_restful import Resource
from application import api
from marshmallow import Schema, fields
from application.utils.SongParser import SongParser


class Playlist(Resource):
    """
    GET endpoint that look like this:
        - api/playlist => returns last 10 songs played on both channels
        - api/playlist/channel1 => returns last 10 songs played on channel1 (default)
        - api/playlist/channel2 => returns last 10 songs played on channel2 (default)
        - api/playlist/channel1?songs=45 => returns last 45 songs played on channel1
        - api/playlist/channel2?songs=45 => returns 10 last songs played on channel1
    """

    class PlaylistSchema(Schema):
        songs = fields.Int()

    schema = PlaylistSchema()
    SONG_HISTORY_DEFAULT = 10

    def get(self, channel=None):
        if channel == None:
            print("none")
            ret = {}
            ret["channel1"] = SongParser.getLastNSongs(self.SONG_HISTORY_DEFAULT, "channel1")
            ret["channel2"] = SongParser.getLastNSongs(self.SONG_HISTORY_DEFAULT, "channel2")
            return ret, 200

        errs = self.schema.validate(request.args)
        if errs:
            abort(400, errs)

        if channel == "channel1":
            return self._getPlaylistForChannel(channel), 200

        if channel == "channel2":
            return self._getPlaylistForChannel(channel), 200


    def _getPlaylistForChannel(self, channel):
            ret = {}
            if request.args.get("songs") == None:
                print("in if _getPla")
                ret[channel] = SongParser.getLastNSongs(self.SONG_HISTORY_DEFAULT, channel)
                return ret
            else:
                print("in else _getPla")
                songs = int(request.args["songs"])
                ret[channel] = SongParser.getLastNSongs(songs, channel), 200
                return ret


api.add_resource(Playlist, "/playlist", "/playlist/<channel>", endpoint="playlist")
