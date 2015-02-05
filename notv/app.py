"""
    notv.app
    ========

    Application factory and settings.

    :copyright: Copyright (c) 2015 Andrey Martyanov. All rights reserved.
    :license: MIT, see LICENSE for more details.
"""

import os

import flask

from .extensions import db, mailgun, migrate
from .views import IndexView


def create_app():
    app = flask.Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY',
        'replace-me-with-real-secret-key')
    if 'NOTV_DEV' in os.environ:
        app.config['DEBUG'] = True
        app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL',
        'sqlite:////tmp/test.db')

    app.config['MAILGUN_DOMAIN'] = os.environ.get('MAILGUN_DOMAIN')
    app.config['MAILGUN_API_KEY'] = os.environ.get('MAILGUN_API_KEY')
    app.config['MAILGUN_DEFAULT_FROM'] = os.environ.get('MAILGUN_DEFAULT_FROM')

    if os.environ.get('NOTV_CONF'):
        app.config.from_envvar('NOTV_CONF')
    else:
        path = os.path.normpath(os.path.expanduser('~/.notv.conf'))
        app.config.from_pyfile(path, silent=True)

    db.init_app(app)
    mailgun.init_app(app)
    migrate.init_app(app, db)

    IndexView.register(app)

    return app
