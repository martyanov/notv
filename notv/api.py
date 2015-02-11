"""
    notv.api
    ========

    RESTful API implementation.

    :copyright: Copyright (c) 2015 Andrey Martyanov. All rights reserved.
    :license: MIT, see LICENSE for more details.
"""

from functools import wraps

from flask import current_app, jsonify, request
from flask.ext.classy import FlaskView

from .models import Show


def auth_required(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_app.config['AUTH_KEY'] != request.args.get('auth_key'):
            r = jsonify(error="unauthorized",
                        message="Please, provide valid 'auth_key'.")
            r.status_code = 401
            return r
        return func(*args, **kwargs)
    return wrapped


class BaseApiView(FlaskView):
    route_prefix = '/api/'
    decorators = [auth_required]


class ShowsApiView(BaseApiView):
    route_base = 'shows'

    def index(self):
        shows = Show.query.all()
        return jsonify(shows=[show.to_dict() for show in shows])
