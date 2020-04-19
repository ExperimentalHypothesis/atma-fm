from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# globally accessible plugins
db = SQLAlchemy()
mail = Mail()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from application import routes

        return app
