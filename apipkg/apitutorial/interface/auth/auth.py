from datetime import datetime, timedelta
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify, make_response
)
from flask_restplus import Resource
import jwt
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from apitutorial.database import get_db
from apitutorial.interface.init_api import api


HASH_ALGO = 'HS256'


ns = api.namespace('auth', description='Operations relating to authorization')


def token_required_user(func):
    @functools.wraps(func)
    def wrapped_view(*args, **kwargs):
        print('*'*79)
        # jwt is passed in the request header
        if 'Authorization' not in request.headers:
            return jsonify({'message' : 'Token is missing. Login first.'}), 401
        token_key = request.headers['Authorization']

        # Using Bearer tokens
        start_str = 'Bearer '
        if not token_key.startswith(start_str):
            return jsonify({'message' : 'Wrong authorization approach!'}), 401
        token = token_key[len(start_str):]
        print(token)

        # Decoding the payload to fetch the stored details
        try:
            data = jwt.decode(token, 'dev', algorithms=HASH_ALGO)#app.config['SECRET_KEY'])
            print(data)
            username = data['username']
        except jwt.exceptions.ExpiredSignatureError:
            abort(401, 'Token has expired. Please login again.')
        except Exception:
            abort(401, 'Token is invalid.')
        # Returns the current logged in users contex to the routes
        return func(username, *args, **kwargs)

    return wrapped_view


@ns.route('/register/')
class RegisterResource(Resource):
    """
    Class Description
    """

    @api.response(204, 'User successfully created.')
    @api.response(401, 'User already exists.')
    def put(self):
        """
        Register a new user.
        """
        rx_json = request.get_json(force=True)

        username = rx_json.get('username', None)
        password = rx_json.get('password', None)

        db = get_db()

        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO user (username, password) VALUES (?, ?)',
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                abort(401, f'User {username} is already registered.')
        else:
            abort(204, f'User {username} is already logged in.')

        return f"User {username} registered.", 204


@ns.route('/login/')
class LoginResource(Resource):
    """
    Class Description
    """

    @api.response(204, 'User successfully created.')
    @api.response(204, 'User is already logged in.')
    @api.response(401, 'Data does not exist.')  # I think this code is right??
    @api.response(401, 'User already exists.')  # I think this code is right??
    def put(self):
        """
        Login request.
        """
        rx_json = request.get_json(force=True)

        if not rx_json or 'username' not in rx_json or 'password' not in rx_json:
            # returns 401 if any email or / and password is missing
            return make_response(
                'Could not verify since PUT request did not have all the necessary information',
                401,
                {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
            )

        username = rx_json['username']
        password = rx_json['password']

        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            # returns 401 if user does not exist
            return make_response(
                'User does not exist',
                401,
                {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
            )

        if not check_password_hash(user['password'], password):
            # Returns 403 if password is wrong
            return make_response(
                'Incorrect password',
                403,
                {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
            )

        # Generates the JWT Token
        payload = {
            'username': username,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }
        token = jwt.encode(payload, 'dev', algorithm=HASH_ALGO)#app.config['SECRET_KEY'])

        return make_response(jsonify({'token' : token}), 201)


@ns.route('/logout/')
class LogoutResource(Resource):
    """
    Class Description
    """

    @api.response(204, 'User logged out')
    def get(self):
        """
        Logout request.
        """
        session.clear()
        return None, 204


