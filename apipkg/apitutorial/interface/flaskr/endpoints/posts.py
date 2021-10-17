#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask_restplus import Resource
from flask import request
from werkzeug.exceptions import abort

from apitutorial.interface.auth.auth import token_required_user
from flask_jwt_extended import get_jwt_identity, jwt_required

from apitutorial.globals import API
from apitutorial.interface.flaskr import common
from apitutorial.interface.flaskr.serializers import flaskr_post


ns = API.namespace('flaskr/posts', description='Operations related to flaskr posts')


@ns.route('/')
class PostListResource(Resource):
    """
    Class Description
    """

    @API.marshal_list_with(flaskr_post)
    @API.response(200, 'Data successfully retreived.')
    def get(self):
        """
        Gets post.
        """
        posts = common.get_posts()
        return posts


@ns.route('/<int:id>/')
class PostResource(Resource):
    """
    Class Description
    """

    @API.marshal_with(flaskr_post)
    @API.response(200, 'Data successfully retreived.')
    def get(self, id):
        """
        Gets post.
        """
        post = common.get_post(id)
        if post is None:
            abort(404, f"Post id {id} doesn't exist.  It may have been deleted.")
        return post

    @jwt_required()
    @API.expect(flaskr_post)
    @API.response(204, 'Post successfully updated.')
    def put(self, id):
        """
        Updates a blog post.
        """
        #update_post(id, data)
        username = get_jwt_identity()
        data = request.get_json()
        
        return None, 204

    @jwt_required
    @API.response(204, 'Post successfully deleted.')
    def delete(self, id, username):
        """
        Deletes blog post.
        """
        print(request.headers)
        username = get_jwt_identity()
        print(username)
        #delete_post(id)
        return None, 204
