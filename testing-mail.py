from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = "experimentalhypothesis@gmail.com"
app.config['MAIL_PASSWORD'] = "Emeraldincubus1"
mail = Mail(app)


@app.route("/")
def index():
    msg = Message("Hello", sender=('Firstname Lastname', 'from@me.com'), recipients=["kotatko.lukas@gmail.com"])
    msg.body = "testing"
    msg.html = "<b>testing</b>"
    mail.send(msg)
    return "sent"


if __name__ == '__main__':
    app.run(debug=True)