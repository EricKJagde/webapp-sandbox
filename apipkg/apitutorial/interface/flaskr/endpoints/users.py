#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask_restplus import Resource
from werkzeug.exceptions import abort

from apitutorial.globals import API
from apitutorial.interface.flaskr import common
from apitutorial.interface.flaskr.serializers import flaskr_user


ns = API.namespace('flaskr/users', description='Operations related to flaskr users')


@ns.route('/')
class UserListResource(Resource):
    """
    Class Description
    """

    @API.marshal_list_with(flaskr_user)
    @API.response(200, 'Data successfully retreived.')
    def get(self):
        """
        Gets users.
        """
        users = common.get_users()
        return users