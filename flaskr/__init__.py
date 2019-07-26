import os

from flask import Flask
from flask_cors import CORS

from flaskr.config import app_config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_DATABASE_URI=f'sqlite:///{app.instance_path}/flaskr.sqlite',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        config_name = os.getenv('APP_SETTINGS', 'production')
        app.config.from_object(app_config[config_name])
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # init db
    from flaskr.db import db
    db.init_app(app)

    # TODO configure cors for security in production
    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.before_first_request
    def create_tables():
        db.create_all()

    # declare endpoints
    from flask_restful import Api
    api = Api(app)

    from flaskr.resources.gif import Gif, GifList
    api.add_resource(Gif, "/gif/<string:id>")
    api.add_resource(GifList, "/gifs")

    from flaskr.resources.category import Category, CategoryList
    api.add_resource(Category, "/category/<string:id>")
    api.add_resource(CategoryList, "/categories")

    from flaskr.resources.user import UserRegister
    api.add_resource(UserRegister, "/register")

    return app
