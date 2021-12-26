from flask import current_app as app


def getCurrentSong() -> dict:
	if app.config['FLASK_ENV'] == 'development':
		return dict(author="name of author", title="name of title")
	else:
		try:
			with open("/opt/ices/log/channel1/ices.cue") as f:
				lines = [line for line in f]
				title = lines[-2].lower()
				author = lines[-1].lower()
				print(title, author)
		except Exception as e:
			print(e)
			return dict(author="name of author", title="name of title")
		return dict(author=author, title=title)



	
	
		




