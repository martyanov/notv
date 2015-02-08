"""
    tests.test_api
    ==============

    API related tests.

    :copyright: Copyright (c) 2015 Andrey Martyanov. All rights reserved.
    :license: MIT, see LICENSE for more details.
"""

import pytest
from flask import json

from notv.app import create_app


@pytest.fixture
def client(request):
    app = create_app()
    app.config['TESTING'] = True
    app.config['AUTH_KEY'] = 'test-key'
    client = app.test_client()
    return client


def test_client_not_authorized(client):
    r = client.get('/api/shows/')
    j = json.loads(r.data)

    assert r.status_code == 401
    assert j['error'] == 'unauthorized'


def test_client_authorized(client):
    r = client.get('/api/shows/?auth_key=test-key')

    assert r.status_code == 200
    assert r.data == b'Shows list'


def test_index_page(client):
    r = client.get('/')

    assert r.status_code == 200
    assert r.data == b'Hello, World!'
