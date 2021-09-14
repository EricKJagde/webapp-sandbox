#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 18:22:18 2021

@author: ericjagde
"""

import sqlite3

import click
"""
g is a special object that is unique for each request. It is used
to store data that might be accessed by multiple functions during
the request. The connection is stored and reused instead of creating
a new connection if get_db is called a second time in the same
request.
"""
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    # open_resource is relative to flaskr
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


"""
with_appcontext is a Flask decorator in the flask.cli module that wraps a
callback to guarantee it will be called with a script's application
context.
"""
@click.command('init-db')  # $ flask init-db on the command line
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    # tells Flask to call that function when cleaning up after returning the response.
    app.teardown_appcontext(close_db)
    # adds a new command that can be called with the flask command.
    app.cli.add_command(init_db_command)