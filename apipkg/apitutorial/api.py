import os

from flask import Flask, Blueprint

from apitutorial import database as db

from apitutorial.interface.init_api import api
from apitutorial.interface.auth.auth import ns as ns_auth
from apitutorial.interface.flaskr.endpoints.posts import ns as ns_flaskr_posts
from apitutorial.interface.flaskr.endpoints.users import ns as ns_flaskr_users


def init_api_app(app):
    # Set up database
    db.init_app(app)

    # Make a blueprint for the api
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(ns_auth)
    api.add_namespace(ns_flaskr_posts)
    api.add_namespace(ns_flaskr_users)
    app.register_blueprint(blueprint)


def main():
    # Create app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Init app
    init_api_app(app)

    # Run app
    app.run(debug=True)


if __name__ == '__main__':
    main()
