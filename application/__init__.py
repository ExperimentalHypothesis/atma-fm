from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# globally accessible plugins
db = SQLAlchemy()
mail = Mail()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    print(app.config)
    # initiating plugins
    db.init_app(app)
    mail.init_app(app)

    # creating application cotext
    with app.app_context():
        from application import routes
        db.create_all()
        return app
