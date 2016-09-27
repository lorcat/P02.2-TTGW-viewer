__author__ = 'Konstantin Glazyrin'

from PyQt4 import QtCore
from app.common import Tester

class ThreadPool(QtCore.QThreadPool, Tester):
    # maximum number of runners
    MAX_THREADS = 5

    # timeout to wait on the runners in ms
    THREAD_TIMEOUT = 3000

    def __init__(self, parent=None):
        Tester.__init__(self)
        QtCore.QThreadPool.__init__(self, parent)

        self.setMaxThreadCount(self.MAX_THREADS)

    def tryStart(self, *args, **kwargs):
        """
        Starts a runner in a thread
        :param runner:
        :return:
        """
        self.debug("Starting a runner ({})".format(args))
        QtCore.QThreadPool.tryStart(self, *args, **kwargs)

    def cleanup(self):
        """
        Cleaning up the procedures
        :return:
        """
        self.waitForDone(self.THREAD_TIMEOUT)

class ProcessRunner(QtCore.QRunnable, Tester):
    """
    Process starting runnable
    """
    def __init__(self, cmd, *args):
        Tester.__init__(self)
        QtCore.QRunnable.__init__(self)

        # save initialization parameters
        self.cmd = cmd
        self.args = args[0]

        if not isinstance(self.args, list) and not isinstance(self.args,tuple):
            self.error("Configuration error; process arguments must be in a list or tuple ({})".format(self.args))
            self.args = []

        self.setAutoDelete(True)

    def run(self):
        """
        Starts a process
        :return:
        """
        self.debug("Starting a process ({}) with arguments ({})".format(self.cmd, self.args))
        proc = QtCore.QProcess()

        proc.startDetached(self.cmd, self.args)

class LambdaRunner(QtCore.QRunnable, Tester):
    """
    Process starting runnable
    """
    def __init__(self, lfunc):
        Tester.__init__(self)
        QtCore.QRunnable.__init__(self)

        # save initialization parameters
        self.cmd = lfunc

        self.setAutoDelete(True)

    def run(self):
        """
        Starts a process
        :return:
        """
        self.debug("Starting a lambda ({})".format(self.cmd))
        self.cmd()

THREAD_POOL = None

def getPool(parent=None):
    global THREAD_POOL
    if THREAD_POOL is None:
        THREAD_POOL = ThreadPool(parent=parent)
    return THREAD_POOL