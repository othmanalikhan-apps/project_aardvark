"""
Controller module of the MVC pattern of the client GUI.

As such, this module controls the transition between GUI components.

In summary, the navigation flow is splash screen ---> multiple tab windows.
"""

__docformat__ = 'reStructuredText'


import os
import sys
import PyQt5
import configparser

from PyQt5.QtWidgets import (
    QApplication, QStyleFactory, QDesktopWidget
)
from src.client.view import (
    MainView
)
from src.client.model import Client


class MainController():
    """
    Controller class of the MVC pattern. Responsible for gluing GUI
    components together.
    """
    def __init__(self):
        """
        Creates the application and main window
        """
        self.app = QApplication(sys.argv)
        self.client = Client(self.getServerSocket())
        self.menu = self.client.requestMenu()
        self.window = MainView(self.menu)

        self.initialiseSettings()
        self.initialiseViewControllers()
        self.exit()

    def initialiseSettings(self):
        """
        Adds plugin folder to path and sets the applications look and feel
        """
        self.app.setStyle(QStyleFactory.create(self.getApplicationStyle()))

    def initialiseViewControllers(self):
        """
        Initialises the controller for each of the views
        """
        self.splashViewController = \
            SplashViewController(self.window.splash, self.window)
#        self.paymentViewController = \
#            PaymentViewController(self.window.tabPayment)
#        self.orderViewController = \
#            OrderViewController(self.window.tabOrder)
#        self.bookingViewController = \
#            BookingViewController(self.window.tabBook)

    def getApplicationStyle(self):
        """
        Attempts to return a preferred style. If not available, returns a default
        os style.
        :return: A style.
        """
        prefStyle = ["Windows"]
        defaultStyle = QStyleFactory.keys()[0]

        prefStyle = [style for style in prefStyle
                     if style in QStyleFactory.keys()]
        prefStyle.append(defaultStyle)

        return prefStyle[0]

    def getServerSocket(self):
        """
        Gets the server socket from the .ini file.
        :return: The server socket in string format.
        """
        path = _getRelativePath('..', '..', 'settings.ini')

        if not os.path.exists(path):
            raise FileNotFoundError("Could not find the settings.ini file!")

        config = configparser.ConfigParser()
        config.read(path)
        return config.get("Network", "serversocket")

    def exit(self):
        """
        Exits the GUI safely by catching the SystemExit exception
        """
        try:
            sys.exit(self.app.exec_())
        except SystemExit:
            print("Exiting Application!")


class SplashViewController:
    """
    Controller for the Splash View widget.
    """

    def __init__(self, splashView, mainWindow):
        """
        Assigns a reference to the splash view widget and the main window.
        Also, assigns event handlers to a button.
        """
        self.mainWindow = mainWindow
        self.splashView = splashView
        self.splashView.clickedContinueButton.connect(
            self.handleContinueButtonClick)

    def handleContinueButtonClick(self):
        """
        Event handler for the the continue button upon clicking.
        """
        self.mainWindow.displayTabs()



def _getRelativePath(*args):
    """
    Gets the relative path to a file.
    (Cross-platform and cross-script compatible)

    :param *args: The relative path to the desired file from the script that
    calls this function (comma separated).
    :return: The absolute path to the desired file.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), *args))

def fixPluginBug():
    """
    Points PyQt to a .dll file that fixes the 'windows' missing plugin bug.
    """
    dirname = os.path.dirname(PyQt5.__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
