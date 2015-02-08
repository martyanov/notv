"""
    notv.views
    ==========

    Project views.

    :copyright: Copyright (c) 2015 Andrey Martyanov. All rights reserved.
    :license: MIT, see LICENSE for more details.
"""

from flask.ext.classy import FlaskView, route


class IndexView(FlaskView):
    route_base = '/'

    @route('/', endpoint='index')
    def index(self):
        return 'Hello, World!'
