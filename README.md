# Online Radio 
Online radio station built on top of the Icecast server using Icegerator as the streaming client. It is a server-centric website bridging backend streaming Icecast server with frontend GUI. It is written in Python Flask with a little bit of vanilla Javascript.

Online radio is broadcasting live 24/7, streaming mostly ambient/experimental/electronic music. All audio files are located on a Fedora VPS server, the code for the website is on the same Fedora VPS server, using NGINX as reverse proxy and Gunicorn as web server.

URL: www.atma-fm.eu

## Clone

You can clone this repo and run it locally even if you do not have Icecast installed. It is recommended to run it on Linux machine although on Windows it should also be possible if you set up correct environment variables (more on that later). Most of the code was actually written on a Windows machine. Follow these steps.

```
git clone https://github.com/ExperimentalHypothesis/flask-online-radio.git
cd flask-online-radio
python -m venv venv
python -r requirements.txt
```

## Install

To run it, you need to first make a .env file where you store environment variables. If you do not set it up, it will not run. You will get an error, most probably SQLAlchemy error because it will not find any path to the database. 

Your .env file should look something like this.

```
ENV = development
SECRET_KEY = somekey
TESTING = True
DEBUG = 0

SQLALCHEMY_DATABASE_URI = sqlite:///somename.db

MAIL_SERVER = smtp.googlemail.com
MAIL_USERNAME = <youremail>@gmail.com
MAIL_PASSWORD = <yourpassword>

LINUX_LOG_PATH = "/some/path/somewhere"
```

The LINUX_LOG_PATH normally points to logfile from Icegenerator. If you do not have it installed, it doesn't matter, the website will still work, the only thing is that you will have an empty playlist. You just have to specify some path, even if it is fictional.

This file has to be located at the root of your application folder (at the same level as run.py file). Be sure you add this .env file to gitignore and never push it to remote repo.

## Run

You can run it by typing 

```
python run.py
```

Be sure that you are inside your virtual environment and your code editor uses the Python interpreter of that environment, otherwise, you can get dependency errors.
