import os

from flask import Blueprint

from apitutorial.globals import APP, API
from apitutorial import database as db_pkg

from apitutorial.interface.auth.auth import ns as ns_auth
from apitutorial.interface.flaskr.endpoints.posts import ns as ns_flaskr_posts
from apitutorial.interface.flaskr.endpoints.users import ns as ns_flaskr_users


def _load_app_config(config=None):
    if config is None:
        APP.config.from_mapping(
            SECRET_KEY='dev',
            JWT_SECRET_KEY='dev',
            DATABASE=os.path.join(APP.instance_path, 'flaskr.sqlite'),
        )
    else:
        # Load other config
        APP.config.from_mapping(config)


def _init_app():
    # Set up database
    db_pkg.init_app(APP)

    # Make a blueprint for the api
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    API.init_app(blueprint)
    API.add_namespace(ns_auth)
    API.add_namespace(ns_flaskr_posts)
    API.add_namespace(ns_flaskr_users)
    APP.register_blueprint(blueprint)


def create_app(config=None):
    # Ensure the instance folder exists
    try:
        os.makedirs(APP.instance_path)
    except OSError:
        pass

    _load_app_config(config)
    _init_app()

    return APP


def main():
    # Init app
    app = create_app()

    # Run app
    app.run(debug=True)


if __name__ == '__main__':
    main()
