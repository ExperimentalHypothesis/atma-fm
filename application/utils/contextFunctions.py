from flask import current_app as app


def getCurrentSong() -> dict:
    MAX_LEN_CURRENT_PLAY = 45

    if app.config["FLASK_ENV"] == "development":
        return dict(author="name of author", title="name of title")
    else:
        try:
            with open("/opt/ices/log/channel1/ices.cue") as f:
                lines = [line for line in f]
                author = lines[-2].lower()
                title = lines[-1].lower()
                both = author +"|"+ title
                if len(both) > MAX_LEN_CURRENT_PLAY:
                    both = both[0:MAX_LEN_CURRENT_PLAY]
                    author = both.split("|")[0]
                    title = both.split("|")[1] + "..."
        except Exception as e:
            return dict(author="unknown artists", title="unknown song")

        return dict(title=title, author=author)