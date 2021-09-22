from flask import request
from flask_restplus import Resource

from api.flaskr.common import get_post, update_post, delete_post
from api.flaskr.serializers import blog_post

from api.restapi import api


ns = api.namespace('flaskr/posts', description='Operations related to blog posts')


@ns.route('/<int:id>')
@api.response(404, 'Post not found.')
class PostItem(Resource):

    @api.marshal_with(blog_post)
    def get(self, id):
        """
        Returns a blog post.
        """
        return get_post(id)

    @api.expect(blog_post)
    @api.response(204, 'Post successfully updated.')
    def put(self, id):
        """
        Updates a blog post.
        """
        data = request.json
        update_post(id, data)
        return None, 204

    @api.response(204, 'Post successfully deleted.')
    def delete(self, id):
        """
        Deletes blog post.
        """
        delete_post(id)
        return None, 204
