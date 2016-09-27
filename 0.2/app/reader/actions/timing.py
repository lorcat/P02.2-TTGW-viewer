__author__ = 'Konstantin Glazyrin'

import time
from app.config.keys import *
from app.common import Tester

def timestamp():
    """
    Returns a timestamp in ms
    :return:
    """

    return ["timestamp", time.time()*1000]


def sleep(duration):
    """
    Sleeps for a given time
    :param timeout: in ms
    :return:
    """
    t = Tester()
    t.makeinfo("Sleeping for ({}ms)".format(duration))

    duration = float(duration)/1000.
    time.sleep(duration)
    return ["sleep", None]

#@TODO: date function