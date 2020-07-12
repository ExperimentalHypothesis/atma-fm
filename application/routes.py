import os

from flask import current_app as app
from flask import send_from_directory
from flask import render_template, request, flash
from flask_mail import Message

from application import mail
from application.models import db, MessageDB
from application.parser import get_last_n_records, parse_record, create_playlist


@app.route('/favicon.ico')
def favicon():
    """ Get favicon icon. """
    return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.context_processor
def get_current_song():
    """ Get currently played song title and artist for main page box. """
    default = dict(author="name of author", title="name of song")
    if app.config['ENV'] == 'development':
        return default
    elif app.config['ENV'] == 'production':
        try:
            title, artist, _, _ = parse_record(get_last_n_records())
        except Exception:
            return default
        return dict(author=artist, title=title)


@app.route("/")
def home():
    """ Route for home page. """
    return render_template("index.html")


@app.route("/about")
def about():
    """ Route for about page. """
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """ Route for contact form. """
    if request.method == 'POST':
        try:
            email = request.form.get("email")
            selection = request.form.get("selection")
            text = request.form.get("text")
            checked = bool(request.form.get("checked"))
            message_db = MessageDB(email=email,
                                   selection=selection,
                                   text=text,
                                   checked=checked)
            db.session.add(message_db)
            db.session.commit()
            if checked:
                msg = Message(subject="regards from atma-fm",
                              sender='atma-fm',
                              reply_to=app.config['MAIL_USERNAME'],
                              recipients=[email])
                # TODO make a email HTML template
                msg.html = f"<div style='font-family: Tomorrow, sans-serif';>thanx for your message,<br> here you have its copy<hr>{text}</div>"

            msg = Message(subject=f"{selection} from form",
                          sender=app.config['MAIL_USERNAME'],
                          reply_to=email,
                          recipients=[app.config['MAIL_USERNAME'], ])
            msg.body = text
            mail.send(msg)
            flash("your message was sent succesfully. bravo!")
            return render_template("contact.html")
        except Exception as e:
            return str(e)
        return render_template("contact.html")


@app.route("/archive")
def archive():
    """ Route for archive page. """
    return render_template("archive.html")


@app.route("/playlist")
def playlist():
    """ Route for playlist page. """
    if app.config["OS"] == "Windows_NT":
        with open(app.config["WINDOWS_LOG_PATH"]) as f:
            lines = []
            for i in range(10):
                lines.append(f.readline())
            print(lines)
            song_history = create_playlist(lines)
    else:
        records = get_last_n_records(path_to_file=app.config["LINUX_LOG_PATH"], n=14)
        song_history = create_playlist(records)
    return render_template("playlist.html", song_history=reversed(song_history))
