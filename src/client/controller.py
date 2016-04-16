"""
Controller module of the MVC pattern of the client GUI.

As such, this module controls the transition between GUI components.

In summary, the navigation flow is splash screen ---> multiple tab windows.
"""

__docformat__ = 'reStructuredText'

import os
import sys
import PyQt5

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QStyleFactory,
    QDesktopWidget
)
from src.client.view import (
    MainTab, getStyle, getSocket, SplashScreen
)


class Controller(QMainWindow):
    """
    Controller class of the MVC pattern. Responsible for gluing GUI
    components together.
    """

    def __init__(self):
        """
        """
        self.initializeSettings()

        super().__init__()
        self.screen = QDesktopWidget()
        self.setCentralWidget(QStackedWidget())

        self.initializeUI()
        self.initializeSplashScreen()
        self.initializeTabs()

        self.show()
        self.exitSafely()


    def initializeSettings(self):
        """
        Initializes GUI settings which includes fixing a path bug, setting
        the GUI app style.
        """
        fixPluginBug()
        self.app = QApplication(sys.argv)
        self.app.setStyle(QStyleFactory.create(getStyle()))

    def initializeUI(self):
        """
        Initializes the GUI UI which includes window title and status bar.
        """
        self.statusBar().showMessage('Ready')
        self.setWindowTitle('Team Aardvark')

    def initializeSplashScreen(self):
        """
        Initializes the splash screen widget.
        """
        self.splash = SplashScreen()
        self.splash.nextButton.clicked.connect(self.handleNextButton)

        self.centralWidget().addWidget(self.splash)
        self.centralWidget().setCurrentWidget(self.splash)
        self.setFixedSize(self.splash.size())

    def initializeTabs(self):
        """
        Initializes the tabs widget.
        """
        self.mainTab = MainTab(getSocket())
        self.centralWidget().addWidget(self.mainTab)

    def handleNextButton(self):
        """
        The handler for the next button for the splash screen which switches
        the splash screen to the main tabs widget.
        """
        width = self.mainTab.size().width()
        height = self.mainTab.size().height()*1.1

        self.centralWidget().setCurrentWidget(self.mainTab)
        self.setMinimumSize(width, height)
        self.setMaximumSize(self.screen.size())

    def exitSafely(self):
        """
        Exits the GUI safely by catching the SystemExit exception
        """
        try:
            sys.exit(self.app.exec_())
        except SystemExit:
            print("Exiting Application!")


def fixPluginBug():
    """
    Points PyQt to a .dll file that fixes the 'windows' missing plugin bug.
    """
    dirname = os.path.dirname(PyQt5.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
