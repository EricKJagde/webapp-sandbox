#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='apipkg',
    version='1.0.0',
    description='REST API',
    author='Eric Jagde',

    classifiers=[
    ],

    keywords='rest restful api flask swagger openapi flask-restplus',

    packages=find_packages(),

    install_requires=['flask-restplus==0.9.2', 'Flask-SQLAlchemy==2.1'],
)