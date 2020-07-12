
# This is a filesystem watchdog responsible for writing from icecast/icegenerator log file to a database.
# Every time the log file changes, icecast log file is the only place where the song history is stored.


from datetime import datetime as dt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from application.models import db, RecordDB
from application.parser import get_last_n_records, parse_record
from application import create_app

app = create_app()

if not app.config["OS"] == "Windows_NT":
    class MyHandler(FileSystemEventHandler):
        """ Class monotoring log file from Icecast server. """

        def on_modified(self, event):
            """ Append currently played song to a database. """
            if event.event_type == "modified" and event.src_path == app.config["LINUX_LOG_PATH"]:
                title, artist, album, started_at = parse_record(get_last_n_records())
                with app.app_context():
                    try:
                        record = RecordDB(title=title,
                                          artist=artist,
                                          album=album,
                                          started_at=started_at,
                                          added_at=dt.now())
                        db.session.add(record)
                        db.session.commit()
                    except Exception as e:
                        print(e)

    def notify():
        """ Get notified when the Icecast log changes. """
        event_handler = MyHandler()
        observer = Observer()
        observer.schedule(event_handler, path="/var/log/icecast/", recursive=False)
        observer.start()