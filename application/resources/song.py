import os
from flask_restful import Resource
from application import api

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
            ret["channel1"] = self._getSongDetails("channel1", self.CUE_FILE_CHANNEL1)
            ret["channel2"] = self._getSongDetails("channel2", self.CUE_FILE_CHANNEL1)
            return ret, 200
        elif channel == "channel1":
            return self._getSongDetails(channel, self.CUE_FILE_CHANNEL1), 200
        elif channel == "channel2":
            return self._getSongDetails(channel, self.CUE_FILE_CHANNEL2), 200
        return {f"msg": "{channel} does not exist"}, 404


    def _getSongDetails(self, channel: str, cueFilepath: str) -> dict:
        ret = {}
        with open(cueFilepath, "r") as f:
            lines = [i.strip() for i in f.readlines()]
            ret["path"] = lines[0]
            ret["size"] = lines[1]
            ret["length"] = lines[3]
            ret["position"] = lines[4]
            ret["bitrate"] = lines[2]
            ret["artist"] = lines[-2]
            ret["album"] = lines[-1]
            ret["channel"] = channel
        return ret

api.add_resource(Song, "/song", "/song/<channel>", endpoint="song")


