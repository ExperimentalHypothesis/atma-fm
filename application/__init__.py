from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()


def create_app():
    """ Initialize app. """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from application import routes  # noqa: F401
        db.create_all()
        return app
