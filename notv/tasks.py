"""
    notv.tasks
    ==========

    Machinery of background tasks.

    :copyright: Copyright (c) 2015 Andrey Martyanov. All rights reserved.
    :license: MIT, see LICENSE for more details.
"""

import logging

from .extensions import mailgun


logger = logging.getLogger(__name__)


def notify_by_email(to, subject, text):
    try:
        mailgun.send_email(to=to, subject=subject, text=text)
        logger.info("Mail to {} successfully sent.".format(to))
    except Exception as e:
        # Flask-Mailgun extension can raise
        # exceptions, we log and pass them silently
        logger.exception(e)
