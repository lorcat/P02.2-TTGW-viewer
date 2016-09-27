__author__ = 'Konstantin Glazyrin'

import time

from app.config.keys import *
from app.config import configuration as config

from app.pytango import CustomProxy
from app.common import Tester

from PyTango import DevState
from PyQt4 import QtGui, QtCore

def read_attribute(device_path, attr, expected_type=float, max=10000, min=-10000):
    """
    Reads an attribute, converts it and outputs it
    :param device_path:
    :param attr:
    :param expected_type: value type to read
    :param max: maximum value to expect, if above that value - reset to default value
    :return:
    """
    res = None
    d = CustomProxy(device_path)

    if not d.isError():
        t = Tester()

        t.debug("main thread ({}); current thread ({})".format(QtGui.QApplication.instance().thread(), QtCore.QThread.currentThread()))

        d.report_device()
        try:
            state = d.state()
            if state != d.FAULT:
                res = d.read_attribute(attr).value
            else:
                t.error("Device has a ({}) state. Aborting the operation.".format(d.FAULT))
        except d.DevFailed:
            t.error("DevFailed upon accessing the device ()".format(d.device_path))
            return

        t.debug("Type of attribute ({}) value is ({})".format(attr, type(res)))

        # test for the maximum and minimum values
        if (t.testFloat(res) or t.testInt(res)) and res > max:
            if res > max or res < min:
                res = None

        if not t.test(res):
            if expected_type is float:
                res = config.CONVERTER[DEFAULT_FLOAT]
            elif expected_type is int:
                res = int(config.CONVERTER[DEFAULT_FLOAT])
            elif expected_type is str:
                res = "NaN"
            elif expected_type == list or expected_type == tuple:
                res = []

    return [READ_ATTRIBUTE, res]

def write_attribute(device_path, attr, value):
    """
    Writes an attribute value
    :param device_path:
    :param attr:
    :param value:
    :return:
    """
    d = CustomProxy(device_path)

    t = Tester()

    if not d.isError():
        d.report_device()
        try:
            state = d.state()
            if state != d.FAULT:
                t.debug("Writing an attribute ({}, {}, {}, {})".format(state, device_path, attr, value))
                d.write_attribute(attr, value)
            else:
                t.error("Device has a ({}) state. Aborting the operation.".format(d.FAULT))
        except d.DevFailed:
            t.error("DevFailed upon accessing the device ()".format(d.device_path))

    return [WRITE_ATTRIBUTE, None]

def write_attribute_asynch(device_path, attr, value):
    """
    Writes an attribute value
    :param device_path:
    :param attr:
    :param value:
    :return:
    """
    d = CustomProxy(device_path)
    t = Tester()

    if not d.isError():
        d.report_device()
        try:
            state = d.state()
            if state != d.FAULT:
                d.write_attribute_asynch(attr, value)
            else:
                t.error("Device has a ({}) state. Aborting the operation.".format(d.FAULT))
        except d.DevFailed:
            t.error("DevFailed upon accessing the device ()".format(d.device_path))

    return [WRITE_ATTRIBUTE_ASYNCH, None]

def command_inout(device_path, cmd, *args):
    """
    Executes a command on the device
    :param device_path:
    :param cmd:
    :param args:
    :return:
    """
    res = None
    d = CustomProxy(device_path)
    t = Tester()

    if not d.isError():
        d.report_device()
        try:
            state = d.state()
            if state != d.FAULT:
                res = d.command_inout(cmd, *args)
            else:
                t.error("Device has a ({}) state. Aborting the operation.".format(d.FAULT))
        except d.DevFailed:
            t.error("DevFailed upon accessing the device ()".format(d.device_path))

    return [COMMAND_INOUT, res]

def command_inout_asynch(device_path, cmd, *args):
    """
    Executes a command on the device in asynch mode
    :param device_path:
    :param cmd:
    :param args:
    :return:
    """
    res = None
    d = CustomProxy(device_path)
    t = Tester()

    if not d.isError():
        d.report_device()
        t.debug("Error state ({})".format(d.isError()))
        try:
            state = d.state()
            if state != d.FAULT:
                res = d.command_inout_asynch(cmd, *args)
            else:
                t.error("Device has a ({}) state. Aborting the operation.".format(d.FAULT))
        except d.DevFailed:
            t.error("DevFailed upon accessing the device ()".format(d.device_path))

    return [COMMAND_INOUT_ASYNCH, res]

def wait_for_state(device_path, timeout, test_state=DevState.ON, sleep_step=300):
    """
    Waits until a certain state is set for a device or until timeout
    :param device_path:
    :param test_state:
    :param timeout: time in ms
    :param sleep_step: time in ms
    :return:
    """
    res = None
    d = CustomProxy(device_path)
    t = Tester()


    t.debug("Waiting for state ({}, DeviceError{})".format(test_state, d.isError()))

    if not d.isError():
        # convert to s
        timeout = float(timeout)/1000.
        sleep_step = float(sleep_step)/1000.

        d.report_device()
        try:
            # test state
            res = d.state()
            if res != d.FAULT:

                # test for a timeout
                counter = 0
                while res != test_state:
                    time.sleep(sleep_step)
                    counter += 1

                    # timeout is None
                    if counter*sleep_step >= timeout:
                        res = None
                        break

                    res = d.state()
                t.debug("Final state reached ({})".format(res))
            else:
                t.error("Device has a ({}) state. Aborting the operation.".format(d.FAULT))
        except d.DevFailed:
            t.error("DevFailed upon accessing the device ()".format(d.device_path))

    return [WAIT_FOR_STATE, res]


_STRING_ATTRIBUTES = {}
def read_attribute_as_string(device_path, attr, form="{}"):
    """
    Reads a string attribute, performes a test for its value change
    :param device_path:
    :param attr:
    :return:
    """
    res = None
    default_res = "-"
    d = CustomProxy(device_path)

    if not d.isError():
        t = Tester()

        # get a value, convert to a string
        d.report_device()
        try:
            state = d.state()
            if state != d.FAULT:
                res = d.read_attribute(attr).value
                res = form.format(res)
            else:
                t.error("Device has a ({}) state. Aborting the operation.".format(d.FAULT))
        except d.DevFailed:
            t.error("DevFailed upon accessing the device ()".format(d.device_path))
            return

        t.debug("Type of attribute ({}) value is ({})".format(attr, type(res)))

        # test for None value
        if not t.test(res):
            res = default_res

        # test for value change, otherwise use
        global _STRING_ATTRIBUTES
        if device_path in _STRING_ATTRIBUTES:
            if _STRING_ATTRIBUTES[device_path] != res:
                _STRING_ATTRIBUTES[device_path] = res
            else:
                res = default_res
        else:
            _STRING_ATTRIBUTES[device_path] = res

    return [READ_ATTRIBUTE, res]