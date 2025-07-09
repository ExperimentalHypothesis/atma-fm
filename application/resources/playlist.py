from flask import request, abort
from flask_restful import Resource
from application import api
from marshmallow import Schema, fields # causing import error ?
from application.utils.SongParser import SongParser


class Playlist(Resource):
    """
    GET endpoint that look like this:
        - api/playlist => returns last 10 songs played on both channels
        - api/playlist/channel1 => returns last 10 (default value) songs played on channel1 
        - api/playlist/channel2 => returns last 10 (default value) songs played on channel2 
        - api/playlist/channel1?songs=N => returns last N songs played on channel1
        - api/playlist/channel2?songs=N => returns last N songs played on channel1
    """

    class PlaylistSchema(Schema):
        songs = fields.Int()

    schema = PlaylistSchema()
    SONG_HISTORY_DEFAULT = 10

    def get(self, channel=None):
        if channel is None:
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
        return None

    def _getPlaylistForChannel(self, channel):
            ret = {}
            if request.args.get("songs") is None:
                print("in if _getPla")
                ret[channel] = SongParser.getLastNSongs(self.SONG_HISTORY_DEFAULT, channel)
                return ret
            else:
                print("in else _getPla")
                songs = int(request.args["songs"])
                ret[channel] = SongParser.getLastNSongs(songs, channel), 200
                return ret

api.add_resource(Playlist, "/playlist", "/playlist/<channel>", endpoint="playlist")
