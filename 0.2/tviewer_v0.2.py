import os
import sys

from app.common import *
from app.common.qt import QtCore, QtGui
from app.config import configuration as config
from app.gui.starter import Starter

# add syspath
sys.path.append(os.path.dirname(__file__))

FILE = __file__

def prepare_resources():
    """
    Updates resources - images and etc. paths
    :return:
    """
    global FILE
    # path to the images
    config.RESOURCES[RESOURCE_IMAGES] = create_path(FILE, "app", "images")

    # path to the htmls
    config.RESOURCES[RESOURCE_HTML] = create_path(FILE, "html")

    # path to the experiment data folder
    config.RESOURCES[RESOURCE_EXPERIMENT] = create_path(FILE, "experiment")

def prepare_profiles():
    """
    Updates profile paths
    :return:
    """
    global FILE
    # directory with profiles
    config.PROFILES[PROFILE_DIR] = create_path(FILE, "profiles")
    # directory with saved profiles - dumps
    config.PROFILES[PROFILE_DIRSAVEDPROFILES] = create_path(FILE, "profiles", "saved")
    # directory for the reports
    config.PROFILES[PROFILE_DIRREPORTS] = create_path(FILE, "reports")

def main():
    """
    Main application file
    :return:
    """
    app = QtGui.QApplication(sys.argv)

    # update resources path
    prepare_resources()

    # update profile path
    prepare_profiles()

    # start splash screen on event loop and then switch to the main app
    o = Starter()

    sys.exit(app.exec_())


if __name__=="__main__":
    main()

#@TODO : save configuration - restore configuration