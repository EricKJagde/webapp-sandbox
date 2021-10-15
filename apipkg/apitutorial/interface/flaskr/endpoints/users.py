#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask_restplus import Resource
from werkzeug.exceptions import abort

from apitutorial.interface.init_api import api
from apitutorial.interface.flaskr import common
from apitutorial.interface.flaskr.serializers import flaskr_user


ns = api.namespace('flaskr/users', description='Operations related to flaskr users')


@ns.route('/')
class UserListResource(Resource):
    """
    Class Description
    """

    @api.marshal_list_with(flaskr_user)
    @api.response(200, 'Data successfully retreived.')
    def get(self):
        """
        Gets users.
        """
        users = common.get_users()
        return users