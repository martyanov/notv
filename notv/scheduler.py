"""
    notv.scheduler
    ==============

    Scheduling facilities.

    :copyright: Copyright (c) 2015 Andrey Martyanov. All rights reserved.
    :license: MIT, see LICENSE for more details.
"""

import time
import threading

import schedule


def run_scheduler(func, period=1):
    schedule.every(period).minutes.do(func)

    def worker():
        while threading.active_count() > 0:
            schedule.run_pending()
            time.sleep(1)

    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
