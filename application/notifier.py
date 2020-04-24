""" 
This is a filesystem watchdog that is responsible for writing from icecast/icegenerator log file to a database every time the log file changes. 
The icecast log file is the only place where the song history is stored.
"""

from datetime import datetime as dt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from application.models import db, RecordDB, LogDB
from application.parser import get_last_n_records, parse_record
from application import create_app

app = create_app()

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.event_type == "modified" and event.src_path == "/var/log/icecast/song-history.log":
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
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='/var/log/icecast', recursive=False)
    observer.start()
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()
    # observer.join()