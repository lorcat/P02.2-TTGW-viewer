__author__ = 'Konstantin Glazyrin'

from app.common import *

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

        # function to be fired on the process finish event
        self.func_finish = None

        if not isinstance(self.args, list) and not isinstance(self.args,tuple):
            self.error("Configuration error; process arguments must be in a list or tuple ({})".format(self.args))
            self.args = []

        self.setAutoDelete(True)

    def setFinishEvent(self, func):
        """
        Sets the function to be fired on the finish event
        :return:
        """
        self.func_finish = func

    def run(self):
        """
        Starts a process
        :return:
        """
        self.debug("Starting a process ({}) with arguments ({})".format(self.cmd, self.args))

        proc = QtCore.QProcess()

        try:
            proc.execute(self.cmd, self.args)
        except TypeError:
            strlist = QtCore.QStringList()
            for el in self.args:
                strlist.append(str(el))
            proc.execute(self.cmd, strlist)

        # synchronous way to wait for the process to finish
        res = proc.waitForFinished(3000)
        self.debug("Process has finished ({})".format(res))
        if self.test(self.func_finish):
            self.debug("Starting ({}) after the process".format(self.func_finish))
            self.func_finish()

THREAD_POOL = None

def get_threadpool(parent=None):
    global THREAD_POOL
    if THREAD_POOL is None:
        THREAD_POOL = ThreadPool(parent=parent)
    return THREAD_POOL