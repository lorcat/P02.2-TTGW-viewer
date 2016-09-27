__author__ = 'Konstantin Glazyrin'

from PyQt4 import QtCore
from app.config.keys import *

MAIN_WINDOW = {
    WINDOW_TITLE : "TTGW Monitor",
}

# logging related configuration
LOGGING = {
    LOGGING_LEVEL: INFO,
}

#### Internal configuration - please do not touch
# profiles
PROFILES = {
    # profile thread priority
    PROFILE_PRIORITY: QtCore.QThread.IdlePriority,

    # profile directory - filled by application
    PROFILE_DIR: None,

    # profile configuration - filled by application
    PROFILE_START: None,

    # reports configuration - filled by application
    PROFILE_DIRREPORTS: None,

    # directory with saved profiles (pickle dumps) - filled by application
    PROFILE_DIRSAVEDPROFILES: None
}


# resources configuration
RESOURCES = {
    # do not change - filled by the application
    RESOURCE_IMAGES: None,

    # path to the HTML files - filled by the application
    RESOURCE_HTML: None,

    # path to the file folder for file saving - filled by the application
    RESOURCE_EXPERIMENT: None
}
