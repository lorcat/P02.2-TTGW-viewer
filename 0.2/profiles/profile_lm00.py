__author__ = 'Konstantin Glazyrin'

from app.common import *
from app.config.keys import *
from app.reader.actions import read_attribute

START = {
    # profile name
    PROFILE_NAME: "P02.2 Camera - LM0",
    # used for file saving purposes
    PROFILE_NICKNAME: "LM00",
    PROFILE_TANGOATTR: [
            # NICK + CMD; CMD - lambda function to execute
            {
                # must be unique
                NICK: "LM00",
                CMD: lambda: read_attribute("haspp02ch2:10000/hasylab/p02_lm0/output", "frame", expected_type=list),

                # parameters for the VIEW ROI - x and y are inverted, w and h are same
                ROI_VIEW:   [ 167, 282,  100, 100],
                PENVIEW: [QtCore.Qt.blue, 1, QtCore.Qt.SolidLine],
            },
    ],

    # profile controllers - applications to run
    PROFILE_CONTROLLERS:  [
                            {CMD:"/usr/bin/gedit", NICK: "Profile editor", ARGS: [__file__.replace("pyc", "py")]},
                            {CMD:"/usr/bin/gnome-terminal", NICK:"Command line", ARGS: []},
                         ],


    # flag controlling application of the ROI view
    PROFILE_SHOW_ROIVIEW: True,

    # View insert position
    PROFILE_INSERT_RECT: [10, 10, 20, 20],

    # View insert position style of the central lines
    PROFILE_INSERTVIEW_LINES: [[255, 0, 0, 100], 1, QtCore.Qt.SolidLine],

    # line style for the center of fit
    PROFILE_INSERTCENTER_LINES: [[150, 200, 255, 255], 1, QtCore.Qt.SolidLine],

    # color lookup table to load by default; Available: thermal; flame; yellowy; bipolar; spectrum; cyclic; greyclip; grey;
    # look at the file pyqtgraph\graphicsItems\GradientEditorItem.py for example - one can create own profile
    PROFILE_COLORTABLE: 'bipolar',

    # delay at which reader tries to access the data
    PROFILE_DELAY: 1000
}
