import requests
from flask import current_app as app
from flask import render_template, Response, request, flash
import random, time, os, random
from application.helpers.parse_song_history import get_last_n_songs
from flask_mail import Message 
from application import mail


# @app.context_processor
# def pass_current_song():
# 	last_played = list(get_last_n_songs(1))
# 	# last_song.author
# 	try:
# 		return dict(author=	last_played[0].author, title=last_played[0].title)
# 	except Exception as e:
# 		print(e, "we are on local dev and this will not work..")

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
	print(app.config)
	if request.method == 'POST':
		print("poslano..")
		try:
			email = request.form.get("email")
			selection = request.form.get("selection")
			text = request.form.get("text")
			checked = request.form.get("checked")
			if checked:
				msg = Message(subject="souvenier from atma-fm", 
							sender='atma-fm',
							reply_to='experimentalbroadcast@gmail.com',
							recipients = [email])

				# msg.body = "thanx for your mesahere you have it\n" + text
				msg.html = f"<div style='font-family: Tomorrow, sans-serif';>thanx for your message,<br> here you have its copy<hr>{text}</div>"	
			msg = Message(subject= f"{selection} from form", 
								sender='experimentalbroadcast@gmail.com',
								reply_to=email,
								recipients = ['experimentalbroadcast@gmail.com'])
			msg.body = text
			print(text)
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
	# song_history = parse_song_history(read_file_from_remote("167.172.122.236", "root", "emeraldincubus"))
	song_history = get_last_n_songs(14)
	return render_template("playlist.html", song_history=song_history)