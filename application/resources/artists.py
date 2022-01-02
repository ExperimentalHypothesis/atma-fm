import os
import pprint
from flask import request, abort
from flask_restful import Resource
from application import api

from marshmallow import Schema, fields


class Artists(Resource):
    """
    GET endpoint looking like this:
        - api/artists => return all artists
        - api/artists?channel=1 => return all artists played on channel1
        - api/artists?channel=2 => return all artists played on channel2
    """

    class ArtistsSchema(Schema):
        channel = fields.Int()

    schema = ArtistsSchema()

    def get(self):

        errs = self.schema.validate(request.args)
        if errs:
            abort(400, errs)

        artistsChannel1 = sorted(os.listdir("/audio/channel1"))
        artistsChannel2 = sorted(os.listdir("/audio/channel2"))
        artistsAll = sorted(artistsChannel1 + artistsChannel2)

        if request.args.get("channel") == None:
            return {"artists": artistsAll}
        elif int(request.args.get("channel")) == 1:
            return {"artists": artistsChannel1}
        elif int(request.args.get("channel")) == 2:
            return {"artists": artistsChannel2}


api.add_resource(Artists, "/artists")
