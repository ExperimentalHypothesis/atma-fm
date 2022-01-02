from flask import Flask
from .utils.contextFunctions import getCurrentSong
from flask_restful import Api

api = Api(prefix="/api")


def create_app():
    app = Flask(__name__)
    import application.resources

    app.config.from_object("config.Config")
    app.context_processor(getCurrentSong)

    api.init_app(app)

    with app.app_context():
        from application import routes

        return app
