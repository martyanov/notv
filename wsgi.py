#!/usr/bin/env python

"""
    wsgi
    ====

    Application WSGI handler.

    :copyright: Copyright (c) 2015 Andrey Martyanov. All rights reserved.
    :license: MIT, see LICENSE for more details.
"""

from notv.app import create_app
from notv.scheduler import run_scheduler


application = create_app()
run_scheduler(lambda: print("Echo"))


if __name__ == '__main__':
    application.run()
