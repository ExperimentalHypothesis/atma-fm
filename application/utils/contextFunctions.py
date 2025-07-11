from flask import current_app as app
from application.constants import MAX_LEN_CURRENT_PLAY, CUE_FILE_CHANNEL1

def get_current_song() -> dict:
    if app.config["FLASK_ENV"] == "development":
        return dict(author="name of author", title="name of title")
    else:
        try:
            print("in get_current_song")
            with open(CUE_FILE_CHANNEL1) as f:
                lines = [line for line in f]
                author = lines[-2].lower()
                title = lines[-1].lower()
                both = author +"|"+ title
                if len(both) > MAX_LEN_CURRENT_PLAY:
                    both = both[0:MAX_LEN_CURRENT_PLAY]
                    author = both.split("|")[0]
                    title = both.split("|")[1] + "..."
        except Exception as e:
            print(e)
            return dict(author="unknown artists", title="unknown song")

        return dict(title=title, author=author)