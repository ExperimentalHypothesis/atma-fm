class SongParser:
    PATH_TO_PLAYLIST = "/opt/icecast/2.4.4/log/playlist.log"

    @classmethod
    def getLastNSongs(cls, n: int, channel: str) -> list:
        records = []
        with open(cls.PATH_TO_PLAYLIST, "r", encoding="unicode_escape") as f:
            for line in f.readlines()[::-1]:
                if channel == "channel1" and "channel1" in line:
                    records.append(line.strip())
                    if len(records) == n:
                        return records
                elif channel == "channel2" and "channel2" in line:
                    records.append(line.strip())
                    if len(records) == n:
                        return records

    @classmethod
    def getSongDetailsFromCue(cls, channel: str, cueFilepath: str) -> dict:
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



if __name__ == "__main__":
    import pprint

    pprint.pprint(SongParser.getLastNSongs(10, 1))
