import os

from flask_restful import Resource
from application import api



class Artists(Resource):
    """
    GET endpoint looking like this:
        - api/artists => return all artists for both channels
        - api/artists/channel1 => return all artists played on channel1
        - api/artists/channel2 => return all artists played on channel2
    """

    @staticmethod
    def get(channel=None):
        ret = {}
        try:
            if channel is None:
                ret["channel1"] = sorted(os.listdir("/audio/channel1"))
                ret["channel2"] = sorted(os.listdir("/audio/channel2"))
            elif channel == "channel1":
                ret["channel1"] = sorted(os.listdir("/audio/channel1"))
            elif channel == "channel2":
                ret["channel2"] = sorted(os.listdir("/audio/channel2"))
            else:
                return {"message": "Channel not found"}, 404
            return ret, 200
        except FileNotFoundError as e:
            return {"message": f"Could not list audio directory: {e}"}, 500

api.add_resource(Artists, "/artists", "/artists/<channel>", endpoint="artists")