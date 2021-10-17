from datetime import datetime, timedelta
import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify, make_response
)
from flask_jwt_extended import create_access_token
from flask_restplus import Resource
import jwt
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash

from apitutorial.database import get_db
from apitutorial.globals import API


HASH_ALGO = 'HS256'


ns = API.namespace('auth', description='Operations relating to authorization')


def token_required_user(func):
    @functools.wraps(func)
    def wrapped_view(*args, **kwargs):
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
            data = jwt.decode(token, 'dev', algorithms=HASH_ALGO)
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

    @API.response(204, 'User successfully created.')
    @API.response(401, 'User already exists.')
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

    @API.response(201, 'Created')
    @API.response(401, 'Unauthorized')
    @API.response(403, 'Forbidden')
    def post(self):
        """
        Login request.
        """
        rx_json = request.get_json(force=True)
        if not rx_json:
            # returns 401 if any email or / and password is missing
            return make_response(
                jsonify({'message': 'No data in request'}), 401
            )

        username = rx_json.get('username', None)
        password = rx_json.get('password', None)
        if username is None or password is None:
            return make_response(
                jsonify({'message': 'Need username and password'}), 401
            )

        db = get_db()
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            return make_response(
                jsonify({'message': 'User does not exist'}), 401
            )

        if not check_password_hash(user['password'], password):
            return make_response(
                jsonify({'message': 'Incorrect password'}), 403
            )

        access_token = create_access_token(
            identity=username,
            expires_delta=timedelta(minutes=30)
        )

        return make_response(
            jsonify({"access_token": access_token}), 201
        )


@ns.route('/logout/')
class LogoutResource(Resource):
    """
    Class Description
    """

    @API.response(204, 'No Content')
    def get(self):
        """
        Logout request.
        """
        session.clear()
        return None, 204


