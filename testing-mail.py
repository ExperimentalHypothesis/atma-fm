# from flask import Flask
# from flask_mail import Mail, Message

# app = Flask(__name__)
# mail = Mail(app)

# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = "kotatko.lukas@gmail.com"
# app.config['MAIL_PASSWORD'] = "724244597"


# @app.route("/")
# def index():
#     msg = Message("Hello", sender="example@gmail.com", recipients=["kotatko.lukas@gmail.com"])
#     msg.body = "testing"
#     msg.html = "<b>testing</b>"
#     mail.send(msg)
#     return "sent"


# if __name__ == '__main__':
#     app.run(debug=True)