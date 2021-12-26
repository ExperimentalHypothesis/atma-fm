
from flask_restful import Resource
from application import api
from application.utils.SongParser import SongParser

class Channel1(Resource):
    def get(self, n):
        l = SongParser.getLastNSongs(n, channel=1)
        return {"songs": l}, 200

class Channel2(Resource):
    def get(self, n):
        l = SongParser.getLastNSongs(n, channel=2)
        return {"songs": l}, 200

api.add_resource(Channel1, "/ch1/<int:n>")
api.add_resource(Channel2, "/ch2/<int:n>")