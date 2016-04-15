import os
import sys

import PyQt5
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QStyleFactory

from src.client.view import View, getStyle, getSocket


def fixPluginBug():
    """
    Points PyQt to a .dll file that fixes the 'windows' missing plugin bug.
    """
    dirname = os.path.dirname(PyQt5.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

def main():
    """
    Sets up the GUI style, configures and then runs it.
    """
    try:
        fixPluginBug()

        app = QApplication(sys.argv)
        app.setStyle(QStyleFactory.create(getStyle()))

        window = View(getSocket())
        window.tabs.show()

        sys.exit(app.exec_())
    except SystemExit:
        print("Exiting Application!")



#http://stackoverflow.com/questions/19966056/
#pyqt5-how-can-i-connect-a-qpushbutton-to-a-slot
