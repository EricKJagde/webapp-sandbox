from flask_restplus import fields

from apitutorial.globals import API


flaskr_post = API.model('Flaskr post', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a blog post'),
    'username': fields.String(required=True, description='Post author'),
    'title': fields.String(required=True, description='Article title'),
    'body': fields.String(required=True, description='Article content'),
    'created': fields.DateTime,
})

flaskr_user = API.model('Flaskr post', {
    'username': fields.String(required=True, description='Post author'),
})