from flask import current_app as app
from flask import render_template

@app.route("/")
def index():
    stream_base_url = app.config['STREAM_SERVER_BASE_URL']
    return render_template("index.html", stream_base_url=stream_base_url)