__author__ = 'glazyrin'

import os
import sys
import logging

from app.config import configuration as config
from app.config.keys import *

try:
    __dl =  config.LOGGING[LOGGING_LEVEL]
except AttributeError:
    __dl = DEBUG

logging.basicConfig(level=__dl,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filemode='w')

LOGGER = None

def get_logger():
    """
    Returns the instance of the logger device to any object asking
    :return:
    """
    global LOGGER
    if LOGGER  is None:
        LOGGER = Logger()
    return LOGGER

# default class for logging information to the STDERR
class Logger():

    DEFAULTLEVEL = DEBUG

    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

        dl = self.DEFAULTLEVEL
        try:
            dl = config.LOGGING[LOGGING_LEVEL]
        except AttributeError:
            pass
        finally:
            self._logger.setLevel(dl)

    @property
    def logger(self):
        return self._logger

    def info(self, msg):
        msg = self._check_msg(msg)
        self._logger.info(msg)

    def debug(self, msg):
        msg = self._check_msg(msg)
        self._logger.debug(msg)

    def error(self, msg):
        msg = self._check_msg(msg)
        self._logger.error(msg)

    def makeinfo(self, msg):
        msg = self._check_msg(msg)
        self._logger.info(msg)

    def warning(self, msg):
        msg = self._check_msg(msg)
        self._logger.error(msg)

    def _check_msg(self, msg):
        if msg is not None:
            if isinstance(msg, str) or isinstance(msg, unicode):
                pass
            else:
                msg = str(msg)
        else:
            msg = str(msg)
        return msg

    def confError(self, key, def_value, e=None):
        self.error("Configuration key {0} does not exist, using default value {1}".format(key, def_value))
        if e is not None:
            self.error("Error message as follows:\n{0}".format(e))

    def confIndexError(self, index, def_value):
        self.error("Configuration index {0} does not exist, reporting default value".format(index, def_value))

    def defFailedError(self, device_path, e=None):
        self.error("Device {0} reports DevFailed error".format(device_path))
        if e is not None:
            self.error("Error message as follows:\n{0}".format(e))

    def set_logfile(self, file_path):
        """
        Sets a logfile
        :return:
        """
        #@TODO: setup a log file
        return


# wrapper to test specific value types
class Tester(Logger):
    def __init__(self):
        Logger.__init__(self)

        self.debug("Class initialization.")

    def test(self, value=None, type=None):
        """
        Main function testing values
        :param value:
        :param type:
        :return:
        """
        res = False

        if value is not None:
            if type is not None and isinstance(value, type):
                res = True
            elif type is None:
                res = True

        return res

    def testString(self, value):
        """
        Tests value for being a string
        :param value:
        :return:
        """
        res = False
        if self.test(value, str) or self.test(value, unicode):
            res = True
        return res

    def testFloat(self, value):
        """
        Tests value for being a float
        :param value:
        :return:
        """
        return self.test(value, float)

    def testInt(self, value):
        """
        Tests value for being an integer
        :param value:
        :return:
        """
        return self.test(value, int)

def create_path(file_path, *args):
    """
    Creates and returns the path based on file name and additional attributes
    :return:
    """
    return os.path.join(os.path.dirname(file_path), *args)
