#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restplus import Api


PATH_ROOT = os.path.split(__file__)[0]


# Create app
APP = Flask(
    __name__,
    instance_path=os.path.join(PATH_ROOT, 'instance'),
    instance_relative_config=True
)

# JSON Web Tokens
JWT = JWTManager(APP)

# Swagger API
API = Api(version='1.0', title='My Blog API',
          description='A simple demonstration of a Flask RestPlus powered API',
          doc='/doc/')