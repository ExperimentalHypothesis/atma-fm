from flask import Flask
from .utils.contextFunctions import get_current_song
from flask_restful import Api

api = Api(prefix="/api")


def create_app():
    app = Flask(__name__)
    import application.resources

    app.config.from_object("config.Config")
    app.context_processor(get_current_song)

    api.init_app(app)

    with app.app_context():
        from application import routes

        return app
