__author__ = 'Konstantin Glazyrin'

from PyTango import *

from app.common import Tester

# implementation of custom proxy to take care for errors and debugging messages
class CustomProxy(DeviceProxy, Tester):

    DevFailed = DevFailed
    FAULT = DevState.FAULT
    MOVING = DevState.MOVING

    def __init__(self, device_path, timeout=1):
        self.device_path = device_path

        Tester.__init__(self)

        try:
            timeout = float(timeout)
        except ValueError:
            timeout = 1

        # error state
        self._error = False
        try:
            DeviceProxy.__init__(self, device_path)
            self.state()
        except (DevFailed, AttributeError) as e:
            self._error = True
            self.error("\nError upon the initialization ({})".format(e))

        self.debug("Initialization of device ({}) has failed ({})".format(self.device_path, self._error))

    def command_inout(self, *args, **kwargs):
        """
        Command inout overload
        """
        self.debug("command_inout ({}, {})".format(str(args), str(kwargs)))
        return DeviceProxy.command_inout(self, *args, **kwargs)

    def command_inout_asynch(self, *args, **kwargs):
        """
        Command inout asynch overload
        """
        self.debug("command_inout_asynch ({}, {})".format(str(args), str(kwargs)))
        return DeviceProxy.command_inout_asynch(self, *args, **kwargs)

    def read_attribute(self, *args, **kwargs):
        """
        read_attribute overload
        """
        self.debug("read_attribute ({}, {})".format(str(args), str(kwargs)))
        return DeviceProxy.read_attribute(self, *args, **kwargs)

    def read_attribute_asynch(self, *args, **kwargs):
        """
        read_attributes_asynch overload
        """
        self.debug("read_attribute_asynch ({}, {})".format(str(args), str(kwargs)))
        return DeviceProxy.read_attribute_asynch(self, *args, **kwargs)

    def write_attribute(self, attr, *args):
        """
        write_attribute overload
        """
        self.debug("write_attribute ({})".format(str(args)))

        return DeviceProxy.write_attribute(self, attr, *args)

    def write_attribute_asynch(self, *args, **kwargs):
        """
        write_attribute_asynch overload
        """
        self.debug("write_attribute ({}, {})".format(str(args), str(kwargs)))
        return DeviceProxy.write_attribute_asynch(self, *args, **kwargs)

    def state(self):
        """
        state() overload
        """
        res = DeviceProxy.state(self)
        self.debug("Device State is ({})".format(res))
        return res

    def report_device(self):
        """
        Outputs the path for the device
        """
        self.debug("Device: ({})".format(self.device_path))

    def debug(self, msg):
        """
        Overload of the debug function
        """
        Tester.debug(self, "{}. {}".format(self.device_path, msg))

    def error(self, msg):
        """
        Overload of the error function
        """
        Tester.error(self, "{}. {}".format(self.device_path, msg))

    def warning(self, msg):
        """
        Overload of the warning function
        """
        Tester.warning(self, "{}. {}".format(self.device_path, msg))

    def isError(self):
        """
        Returns the state of error
        :return:
        """
        return self._error

# @TODO: Implement timeout for device connection