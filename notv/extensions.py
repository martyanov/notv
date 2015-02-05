"""
    notv.extensions
    ===============

    Extensions factory.

    :copyright: Copyright (c) 2015 Andrey Martyanov. All rights reserved.
    :license: MIT, see LICENSE for more details.
"""

from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy
from flask_mailgun import Mailgun


db = SQLAlchemy()
mailgun = Mailgun()
migrate = Migrate()
