import os
from difflib import get_close_matches
from flask_restful import Resource
from application import api


class Albums(Resource):
    """
    GET endpoint looking like this:
        - api/albums/<artist_name> => return all albums from particular artist with channel where they are played on
    """

    def get(self, artist):
        val = {"channel1": self._get_albums_for_channel(artist, "/audio/channel1"),
               "channel2": self._get_albums_for_channel(artist, "/audio/channel2")}
        return {artist: val}, 200


    @staticmethod
    def _get_albums_for_channel(artist, channel_path):
        # --- This logic is now safely inside the request method ---
        try:
            all_artists_in_channel = os.listdir(channel_path)
            # Find the correct case for the artist's directory name
            matching_artist = next((a for a in all_artists_in_channel if a.lower() == artist.lower()), None)

            if matching_artist:
                artist_path = os.path.join(channel_path, matching_artist)
                return [album for album in os.listdir(artist_path) if os.path.isdir(os.path.join(artist_path, album))]

            # Suggest close matches if no exact match is found
            matches = get_close_matches(artist, all_artists_in_channel, cutoff=0.7)
            if matches:
                return f"{artist} not found, did you mean {matches}?"
            return f"{artist} not found"
        except FileNotFoundError:
            return f"Directory for channel '{channel_path}' not found."


api.add_resource(Albums, "/albums/<artist>")