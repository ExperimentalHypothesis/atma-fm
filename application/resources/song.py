import os
from flask_restful import Resource
from application import api
from application.utils.SongParser import SongParser

class Song(Resource):
    """
        GET endpoint looking like this:
        -api/song => return song details from cue file for both channels (default)
        -api/song/channel1 => return song details from cue file from channel1
        -api/song/channel2 => return song details from cue file from channel2
    """
    
    CUE_FILE_CHANNEL1 = r"/opt/ices/log/channel1/ices.cue"
    CUE_FILE_CHANNEL2 = r"/opt/ices/log/channel2/ices.cue"
    
    def get(self, channel=None):
        if channel == None:
            ret = {}
            ret["channel1"] = SongParser.getSongDetailsFromCue("channel1", self.CUE_FILE_CHANNEL1)
            ret["channel2"] = SongParser.getSongDetailsFromCue("channel2", self.CUE_FILE_CHANNEL1)
            return ret, 200
        elif channel == "channel1":
            return SongParser.getSongDetailsFromCue(channel, self.CUE_FILE_CHANNEL1), 200
        elif channel == "channel2":
            return SongParser.getSongDetailsFromCue(channel, self.CUE_FILE_CHANNEL2), 200
        return {f"msg": "{channel} does not exist"}, 404

api.add_resource(Song, "/song", "/song/<channel>", endpoint="song")


