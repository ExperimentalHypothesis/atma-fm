import requests
from app import app
from flask import render_template, Response, request, flash
import random, time, os, random
from app.helpers.parse_song_history import get_last_n_songs
from flask_mail import Message, Mail

app.config['SECRET_KEY'] = 'b36e4ef7cd15862acf8e3cb9ea4bc59a'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'experimentalbroadcast@gmail.com'
app.config['MAIL_PASSWORD'] = 'xxxxx'
mail = Mail(app)

# on local dev this has to commented out, otherwise it will throw error (no connection to streaming server)
@app.context_processor
def pass_current_song():
	last_played = list(get_last_n_songs(1))
	# last_song.author	
	return dict(author=last_played[0].author, title=last_played[0].title)

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
