"""
    notv.models
    ===========

    Models declaration.

    :copyright: Copyright (c) 2015 Andrey Martyanov. All rights reserved.
    :license: MIT, see LICENSE for more details.
"""

from .extensions import db


class Show(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, unique=True, nullable=False, index=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    latest_episode_date = db.Column(db.Date)
    next_episode_date = db.Column(db.Date)
    is_ended = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Show feed_id={} name={}>".format(self.feed_id, self.name)
