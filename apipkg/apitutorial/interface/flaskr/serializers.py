from flask_restplus import fields

from apitutorial.interface.init_api import api


flaskr_post = api.model('Flaskr post', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a blog post'),
    'username': fields.String(required=True, description='Post author'),
    'title': fields.String(required=True, description='Article title'),
    'body': fields.String(required=True, description='Article content'),
    'created': fields.DateTime,
})

flaskr_user = api.model('Flaskr post', {
    'username': fields.String(required=True, description='Post author'),
})