#!/usr/bin/env python3

import os
import sys
import signal

import rospy
import rospkg

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget, QFileDialog, QMessageBox

from std_msgs.msg import String

class RqtTablesDemo(Plugin):

    def __init__(self, context):
        super(RqtTablesDemo, self).__init__(context)
        rospy.loginfo('Initializing rqt_tables_demo, have a happy pick, place and move and more!')

        self.setObjectName('RqtTablesDemo')
        # Create QWidget
        self._widget = QWidget()
        # Get path to UI file (xml description of the gui window created with qtcreator)
        ui_file = os.path.join(rospkg.RosPack().get_path('rqt_tables_demo'), 'config', 'rqt_tables_demo.ui')
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self._widget)
        self._widget.setObjectName('rqt_tables_demo.ui')
        # Show _widget.windowTitle on left-top of each plugin (when
        # it's set in _widget). This is useful when you open multiple
        # plugins at once. Also if you open multiple instances of your
        # plugin at once, these lines add number to make it easy to
        # tell from pane to pane.
        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))

        # class variables
        # self.foo = None

        # publications
        # self.object_mesh_pub = rospy.Publisher('my_topic', String, queue_size=1)

        # parameters
        # foo_param = rospy.get_param('foo_param', 'default_value')

        ## make a connection between the qt objects and this class methods
        self._widget.cmdHi.clicked.connect(self.foo)

        context.add_widget(self._widget)

        # to catch Ctrl + C signal from keyboard and close stream properly
        signal.signal(signal.SIGINT, self.signal_handler)

        rospy.loginfo('rqt initialized')
        # end of constructor

    # ::::::::::::::  class methods

    def shutdown_plugin(self):
        rospy.loginfo('I detected you want to quit, calling destructor')
        self.__del__()

    def signal_handler(self, sig, frame):
        rospy.loginfo('You pressed Ctrl+C, calling destructor')
        self.__del__()

    def __del__(self):
        '''
        Destructor
        '''
        # TODO: perform cleanup
        rospy.loginfo('bye bye!')
        sys.exit(0)

    def foo(self):
        rospy.loginfo('Hi!')
