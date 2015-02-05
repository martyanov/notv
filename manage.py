"""
    manage
    ======

    Collection of helpers to manage database migrations, shell access, etc.

    :copyright: Copyright (c) 2015 Andrey Martyanov. All rights reserved.
    :license: MIT, see LICENSE for more details.
"""

from flask.ext.migrate import MigrateCommand
from flask.ext.script import Shell, Manager

from notv import models
from notv.app import create_app
from notv.extensions import db


app = create_app()


def _make_context():
    return dict(app=app, db=db, models=models)


manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("shell", Shell(make_context=_make_context))


if __name__ == '__main__':
    manager.run()
