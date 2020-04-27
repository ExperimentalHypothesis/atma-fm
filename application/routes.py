import requests
import random, time, os, random

from flask import current_app as app
from flask import render_template, Response, request, flash
from flask_mail import Message 

# from application.helpers.parse_song_history import get_last_n_songs
from application import mail
from application.models import db, MessageDB, RecordDB, LogDB
from application.parser import get_last_n_records, parse_record, create_playlist
from flask import current_app as app

@app.context_processor
def pass_current_song():
	if app.config['ENV'] == 'development':
		return dict(author="name of author", title="name of song")
	elif app.config['ENV'] == 'production':
		try:
			title, artist, _, _ = parse_record(get_last_n_records())
		except Exception:
			return dict(author="name of author", title="name of song")
		return dict(author=artist, title=title)


@app.route("/")
def home():
	return render_template("index.html")


@app.route("/about")
def about():
	return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
	if request.method == 'POST':
		try:
			email = request.form.get("email")
			selection = request.form.get("selection")
			text = request.form.get("text")
			checked = bool(request.form.get("checked"))

			# save the message to the database
			message_db = MessageDB(email=email,
									selection=selection, 
									text=text,
									checked=checked)
			db.session.add(message_db)
			db.session.commit()

			# send a copy to the client
			if checked:
				msg = Message(subject="regards from atma-fm", 
								sender='atma-fm',
								reply_to=app.config['MAIL_USERNAME'],
								recipients = [email])
				msg.html = f"<div style='font-family: Tomorrow, sans-serif';>thanx for your message,<br> here you have its copy<hr>{text}</div>"

			msg = Message(subject= f"{selection} from form", 
								sender=app.config['MAIL_USERNAME'],
								reply_to=email,
								recipients=[app.config['MAIL_USERNAME'],])
			msg.body = text
			mail.send(msg)
			flash("your message was sent succesfully. bravo!")
			return render_template("contact.html")
		except Exception as e:
			return str(e)
	return render_template("contact.html")


@app.route("/archive")
def archive():
	return render_template("archive.html")


@app.route("/playlist")
def playlist():
	if app.config["OS"] == "Windows_NT":
		with open(r"C:\Users\nirvikalpa\source\repos\Python\flask-online-radio\_windows_fake_log.log") as f:
			lines = []
			for i in range(10):
				lines.append(f.readline())
			print(lines)
			song_history = create_playlist(lines)
		return render_template("playlist.html", song_history=song_history)
	else:
		records = get_last_n_records(n=10)
		song_history = create_playlist(records)
	return render_template("playlist.html", song_history=song_history)

