#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask_restplus import Resource
from werkzeug.exceptions import abort

from apitutorial.interface.auth.auth import token_required

from apitutorial.interface.init_api import api
from apitutorial.interface.flaskr import common
from apitutorial.interface.flaskr.serializers import flaskr_post


ns = api.namespace('flaskr/posts', description='Operations related to flaskr posts')


@ns.route('/')
class PostListResource(Resource):
    """
    Class Description
    """

    @token_required
    @api.marshal_list_with(flaskr_post)
    @api.response(200, 'Data successfully retreived.')
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

    @api.marshal_with(flaskr_post)
    @api.response(200, 'Data successfully retreived.')
    def get(self, id):
        """
        Gets post.
        """
        post = common.get_post(id)
        if post is None:
            abort(404, f"Post id {id} doesn't exist.  It may have been deleted.")
        return post

    @api.expect(flaskr_post)
    @api.response(204, 'Post successfully updated.')
    def put(self):
        """
        Updates a blog post.
        """
        #data = request.json
        #update_post(id, data)
        return None, 204

    @api.response(204, 'Post successfully deleted.')
    def delete(self, id):
        """
        Deletes blog post.
        """
        #delete_post(id)
        return None, 204
