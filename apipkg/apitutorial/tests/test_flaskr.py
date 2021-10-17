#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import tempfile

import pytest

from apitutorial.api import create_app
from apitutorial import database as db_pkg


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            db_pkg.init_db_test()
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_empty_db(client):
    """Start with a blank database."""

    # Somehow use client

    assert True