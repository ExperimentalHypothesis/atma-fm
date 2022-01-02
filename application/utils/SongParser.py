class SongParser:
    pathToPlaylist = "/opt/icecast/2.4.4/log/playlist.log"

    @classmethod
    def getLastNSongs(cls, n: int, channel: int) -> list:
        records = []
        with open(cls.pathToPlaylist, "r", encoding="unicode_escape") as f:
            for line in f.readlines()[::-1]:
                if channel == 1 and "channel1" in line:
                    records.append(line)
                    if len(records) == n:
                        return records
                elif channel == 2 and "channel2" in line:
                    records.append(line)
                    if len(records) == n:
                        return records


if __name__ == "__main__":
    import pprint

    pprint.pprint(SongParser.getLastNSongs(10, 1))
