__author__ = 'Konstantin Glazyrin'

import time
from math import *
import random

from PyTango import DevState

from app.config.keys import *
from app.config import configuration as config

from app.pytango import CustomProxy
from app.common import Tester

def read_attribute(device_path, attr):
    """
    Reads an attribute, converts it and outputs it
    :param device_path:
    :param attr:
    :return:
    """
    res = random.randint(0, 10)
    t = Tester()

    ftype = READ_ATTRIBUTE
    t.debug("{} ({})".format(ftype, res))

    return [ftype, res]

def write_attribute(device_path, attr, value):
    """
    Writes an attribute value
    :param device_path:
    :param attr:
    :param value:
    :return:
    """
    t = Tester()

    ftype = WRITE_ATTRIBUTE
    t.debug("{} ({}, {}, {})".format(ftype, device_path, attr, value))

    return [ftype, None]

def write_attribute_asynch(device_path, attr, value):
    """
    Writes an attribute value
    :param device_path:
    :param attr:
    :param value:
    :return:
    """
    t = Tester()

    ftype = WRITE_ATTRIBUTE_ASYNCH
    t.debug("{} ({}, {}, {})".format(ftype, device_path, attr, value))

    return [ftype, None]

def command_inout(device_path, cmd, *args):
    """
    Executes a command on the device
    :param device_path:
    :param cmd:
    :param args:
    :return:
    """
    res = random.randint(0, 1)
    t = Tester()

    ftype = COMMAND_INOUT
    t.debug("{} ({}, {}, {})".format(ftype, device_path, cmd, str(*args)))

    return [ftype, res]

def command_inout_asynch(device_path, cmd, *args):
    """
    Executes a command on the device in asynch mode
    :param device_path:
    :param cmd:
    :param args:
    :return:
    """
    res = random.randint(0, 1)
    t = Tester()

    ftype = COMMAND_INOUT_ASYNCH
    t.debug("{} ({}, {}, {})".format(ftype, device_path, cmd, str(*args)))

    return [ftype, res]

def wait_for_state(device_path, test_state, timeout, sleep_step=200):
    """
    Waits until a certain state is set for a device or until timeout
    :param device_path:
    :param test_state:
    :param timeout: time in ms
    :param sleep_step: time in ms
    :return:
    """
    t = Tester()
    res = DevState.ON

    ftype = WAIT_FOR_STATE
    t.debug("{} ({}, {}, {}, {})".format(ftype, device_path, test_state, timeout, sleep_step))

    return [ftype, res]
