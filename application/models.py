from application import db

class SongDB(db.Model):
    """ Data model for songs broadcasted on stream """

    __tablename__ = "playlist"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=False, nullable=False)
    artist = db.Column(db.String(64), unique=False, nullable=False)
    album = db.Column(db.String(64), unique=False, nullable=False)
    started = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'Song {self.id}, {self.title}, {self.artist}, {self.album}, {self.started}'



class MessageDB(db.Model):
    """ Data model for messages sent via contact form """

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=False, nullable=True)
    selection = db.Column(db.String(32), unique=False, nullable=False)
    text = db.Column(db.Text, unique=False, nullable=True)
    checked = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return f'Message {self.id}, {self.email}, {self.selection}, {self.text}'
    

    

