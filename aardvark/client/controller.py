"""
Controller module of the MVC pattern of the client GUI.

As such, this module controls the transition between GUI components.

In summary, the navigation flow is splash screen ---> multiple tab windows.
"""

__docformat__ = 'reStructuredText'

import os
import sys
import configparser
import collections

from PyQt5.QtWidgets import (
    QApplication, QStyleFactory
)
from aardvark.client.view import (
    MainView
)
from aardvark.client.model import Client


class MainController:
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
#        self.totalTables = self.client.requestTotalTables()
        self.window = MainView(self.menu, 200)

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
        self.splashViewController = SplashViewController(self.window.splash, self.window)
        self.paymentViewController = PaymentViewController(self.window.tabPayment)
        self.orderViewController = OrderViewController(self.window.tabOrder)
        self.bookingViewController = BookingViewController(self.window.tabBook)

    def getApplicationStyle(self):
        """
        Attempts to return a preferred style. If not available, returns a
        default os style.

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

        :param splashView: An instantiated SplashView object.
        :param mainWindow: An instantiated QWidget that is the MainWindow.
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


class OrderViewController:
    """
    Controller for the Order View widget.
    """

    def __init__(self, orderView):
        """
        Constructor that mainly connects buttons to handlers.

        :param orderView: An instantiated OrderView object.
        """
        self.orderedItems = collections.OrderedDict()
        self.orderView = orderView
        self.orderView.tableScreen.clickedTableButton.connect(self.handleTableButtonClick)
        self.orderView.orderScreen.clickedFoodButton.connect(self.handleFoodButtonClick)
        self.orderView.orderScreen.clickedSubtractButton.connect(self.handleSubtractButton)
        self.orderView.orderScreen.clickedAddButton.connect(self.handleAddButton)
        self.orderView.orderScreen.clickedBackButton.connect( self.handleBackButtonClick)
        self.orderView.orderScreen.clickedSubmitButton.connect(self.handleSubmitButtonClick)

    def handleFoodButtonClick(self, foodName):
        """
        Event handler that adds items to the ordered items and displays
        the updated ordered items on the screen.

        :param foodName: The name of the food.
        """
        if foodName in self.orderedItems:
            self.orderedItems[foodName] += 1
        else:
            self.orderedItems[foodName] = 1

        self.orderView.orderScreen.displayOrderedItems(self.orderedItems)

    def handleTableButtonClick(self, tableNumber):
        """
        Event handler for that switches the current displayed widget to the
        order screen.

        :param tableNumber: The number of the table.
        """
        self.orderView.displayOrderScreen(tableNumber)

    def handleSubmitButtonClick(self):
        """
        Event handler for that
        """
        print("You've clicked the submit button")

    def handleBackButtonClick(self):
        """
        Event handler for that switches the current displayed widget to the
        table screen.
        """
        self.orderView.displayTableScreen()

    def handleSubtractButton(self, foodName):
        """
        Event handler that removes items from the ordered items and displays
        the updated results on screen.

        :param foodName: The name of the food.
        """
        if foodName in self.orderedItems:
            self.orderedItems[foodName] -= 1
            if self.orderedItems[foodName] <= 0:
                self.orderedItems.pop(foodName)

        self.orderView.orderScreen.displayOrderedItems(self.orderedItems)

    def handleAddButton(self, foodName):
        """
        Event handler that adds items from the ordered items and displays
        the updated results on screen.

        :param foodName: The name of the food.
        """
        if foodName in self.orderedItems:
            self.orderedItems[foodName] += 1

        self.orderView.orderScreen.displayOrderedItems(self.orderedItems)


class BookingViewController:
    """
    Controller for the Order View widget.
    """

    def __init__(self, bookingView):
        """
        Constructor that mainly connects buttons to handlers.

        :param bookingView: An instantiated BookingView object.
        """
        self.bookingView = bookingView
        self.bookingView.clickedBookingButton.connect(self.handleBookingButtonClick)

    def handleBookingButtonClick(self, customerName, customerPhone, customerEmail,
                                            bookingDate, bookingTime, bookingTable):
        print("Name: " + customerName)
        print("Phone: " + customerPhone)
        print("Email: " + customerEmail)
        print("Date: " + bookingDate.toString())
        print("Time: " + bookingTime)
        print("Table: " + bookingTable)


class PaymentViewController:
    """
    Controller for the Payment View widget.
    """

    def __init__(self, paymentView):
        """
        Constructor that mainly connects buttons to handlers.

        :param paymentView: An instantiated PaymentView object.
        """
        self.paymentView = paymentView
        self.paymentView.tableScreen.clickedTableButton.connect(self.handleTableButtonClick)
        self.paymentView.paymentScreen.clickedBackButton.connect(self.handleBackButtonClick)
        self.paymentView.paymentScreen.clickedPayButton.connect(self.handlePayButtonClick)
        self.paymentView.paymentScreen.clickedPrintButton.connect(self.handlePrintButtonClick)

    def handlePrintButtonClick(self):
        print("You've clicked the print button")

    def handlePayButtonClick(self):
        print("You've clicked the pay button")

    def handleBackButtonClick(self):
        """
        Event handler for that switches the current displayed widget to the
        table screen.
        """
        self.paymentView.displayTableScreen()

    def handleTableButtonClick(self, tableNumber):
        """
        Event handler that switches the current displayed widget to the
        payment screen.

        :param tableNumber: The number of the table.
        """
        self.paymentView.displayPaymentScreen(tableNumber)


def _getRelativePath(*args):
    """
    Gets the relative path to a file.
    (Cross-platform and cross-script compatible)

    :param *args: The relative path to the desired file from the script that
    calls this function (comma separated).
    :return: The absolute path to the desired file.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), *args))

#def fixPluginBug():
#    """
#    Points PyQt to a .dll file that fixes the 'windows' missing plugin bug.
#    """
#    dirname = os.path.dirname(PyQt5.__file__)
#    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
#    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
