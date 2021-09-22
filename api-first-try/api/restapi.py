from flask_restplus import Api
from rest_api_demo import settings


api = Api(version='1.0', title='My Blog API',
          description='A simple demonstration of a Flask RestPlus powered API')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500
