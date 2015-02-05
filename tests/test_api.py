"""
    tests.test_api
    ==============

    API related tests.

    :copyright: Copyright (c) 2015 Andrey Martyanov. All rights reserved.
    :license: MIT, see LICENSE for more details.
"""

import pytest

from notv.app import create_app


@pytest.fixture
def client(request):
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    return client


def test_index_page(client):
    r = client.get('/')
    assert r.status_code == 200
    assert r.data == b'Hello, World!'
