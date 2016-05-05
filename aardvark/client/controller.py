"""
Controller module of the MVC pattern of the client GUI.

As such, this module controls the transition between GUI components.

In summary, the navigation flow is splash screen ---> multiple tab windows.
"""
import json
import re

import requests

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
        self.splashViewController = \
            SplashViewController(self.window.splash, self.window)
        self.paymentViewController = \
            PaymentViewController( self.window.tabPayment, self.client)
        self.orderViewController = \
            OrderViewController(self.window.tabOrder, self.client)
        self.bookingViewController = \
            BookingViewController(self.window.tabBook, self.client)

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

    def __init__(self, orderView, client):
        """
        Constructor that mainly connects buttons to handlers.

        :param orderView: An instantiated OrderView object.
        :param client: The client that deals with the communicating to the
        server.
        """
        self.orderedItems = collections.OrderedDict()
        self.orderView = orderView
        self.orderView.tableScreen.clickedTableButton.connect(self.handleTableButtonClick)
        self.orderView.orderScreen.clickedFoodButton.connect(self.handleFoodButtonClick)
        self.orderView.orderScreen.clickedSubtractButton.connect(self.handleSubtractButton)
        self.orderView.orderScreen.clickedAddButton.connect(self.handleAddButton)
        self.orderView.orderScreen.clickedBackButton.connect( self.handleBackButtonClick)
        self.orderView.orderScreen.clickedSubmitButton.connect(self.handleSubmitButtonClick)
        self.client = client

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
        Event handler that submits all items in the order items basket to the
        server.
        """
        response = self.client.submitOrder(self.orderedItems)
        if response.status_code == requests.codes.ok:
            self.orderedItems = {}
            self.orderView.orderScreen.displayOrderedItems(self.orderedItems)
            self.orderView.orderScreen.showSuccessPopup()
        else:
            self.orderView.orderScreen.showFailPopup()


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

    def __init__(self, bookingView, client):
        """
        Constructor that mainly connects buttons to handlers.

        :param bookingView: An instantiated BookingView object.
        :param client: The client that deals with the communicating to the
        server.
        """
        self.bookingView = bookingView
        self.bookingView.clickedBookingButton.connect(self.handleBookingButtonClick)

        self.bookingView.clickedDateEdit.connect(self.handleDateEditClick)
        self.dateEditClickedTimes = 0

        self.bookingView.clickedTimeField.connect(self.handleTimeFieldClick)
        self.timeFieldClickedTimes = 0

        self.bookingView.clickedSizeField.connect(self.handleSizeFieldClick)
        self.sizeFieldClickedTimes = 0

#        self.tableFieldClickedTimes = 0
#        self.bookingView.clickedTableField.connect(self.handleTableFieldClick)

        self.client = client

    def handleBookingButtonClick(self,
                                 customerName,
                                 customerEmail,
                                 customerPhone,
                                 bookingDate,
                                 bookingTime,
                                 bookingTable,
                                 bookingSize):
        """
        Event handler for clicking the booking button.
        Sanitizes the user input then proceeds to send the data to the server.

        :param customerName: name of the customer.
        :param customerEmail: email of the customer.
        :param customerPhone: phone number of the customer.
        :param bookingDate: the booking date.
        :param bookingTime: the booking time.
        :param bookingTable: the booked table.
        :param bookingSize: the amount of seats book.
        """
        bookingDetails = {"name": customerName.lower(),
                          "email": customerEmail.lower(),
                          "phone": customerPhone,
                          "date": bookingDate,
                          "time": bookingTime,
                          "table": bookingTable,
                          "size": bookingSize}

        if not self._validateEmptyFields():
            self.bookingView.showEmptyFieldsPopup()
        elif not self._validateEmail():
            self.bookingView.showInvalidEmailPopup()
        elif not self._validatePhoneNumber():
            self.bookingView.showInvalidPhonePopup()
        else:
            response = self.client.sendBookingDetails(**bookingDetails)
            data = json.loads(response.content.decode("utf-8"))

            self.bookingView.setBookingStatusText(data["reference"])
            self.bookingView.tableField.clear()

    def handleDateEditClick(self):
        """
        Event handler for clicking on the date widget.
        Sets the size time widget to enabled to allow entering of input
        and fetches data for that field form the server.
        """
        # Fixed unchanging times, or so it is assumed
        TIMES = ["09:00", "11:00", "13:00", "15:00"]
        self.bookingView.timeField.clear()
        self.bookingView.timeField.addItems(TIMES)
        self.bookingView.timeField.setDisabled(False)

    def handleTimeFieldClick(self):
        """
        Event handler for clicking on the time field widget.
        Sets the size field widget to enabled to allow entering of input
        and fetches data for that field from the server.
        """
        date = self.bookingView.getBookingDate()
        time = self.bookingView.getBookingTime()
        sizes = self.client.requestAvailableSizes(date, time)
        self.bookingView.sizeField.clear()
        self.bookingView.sizeField.addItems(sizes)
        self.bookingView.sizeField.setDisabled(False)

        self.bookingView.tableField.setDisabled(True)
        self.bookingView.tableField.clear()

    def handleSizeFieldClick(self):
        """
        Event handler for clicking on the size field widget.
        Sets the time field widget to enabled to allow entering of input
        and fetches data for that field from the server.
        """
        date = self.bookingView.getBookingDate()
        time = self.bookingView.getBookingTime()
        size = self.bookingView.getBookingSize()
        tables = self.client.requestAvailableTables(date, time, size)
        self.bookingView.tableField.clear()
        self.bookingView.tableField.addItems(tables)
        self.bookingView.tableField.setDisabled(False)

    def _validateEmail(self):
        """
        Checks whether the supplied email is valid.

        :return: boolean true or false.
        """
        EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+"
                                 r"\.[a-zA-Z0-9-.]+$)")
        isEmailValid =  re.match(EMAIL_REGEX,
                                 self.bookingView.getCustomerEmail())
        return isEmailValid

    def _validatePhoneNumber(self):
        """
        Checks whether the supplied number is valid.

        :return: boolean true or false.
        """
        NUMBER_REGEX = re.compile(r"^[0-9]{7,12}$")
        isNumberValid =  re.match(NUMBER_REGEX,
                                  self.bookingView.getCustomerPhone())
        return isNumberValid

    def _validateEmptyFields(self):
        """
        Checks whether all fields are non empty.

        :return: boolean true or false.
        """
        validationFields = [self.bookingView.getCustomerName(),
                            self.bookingView.getCustomerEmail(),
                            self.bookingView.getCustomerPhone(),
                            self.bookingView.getBookingDate(),
                            self.bookingView.getBookingTime(),
                            self.bookingView.getBookingSize(),
                            self.bookingView.getBookingTable()]

        for field in validationFields:
            if not field:
                return False
        return True


class PaymentViewController:
    """
    Controller for the Payment View widget.
    """

    def __init__(self, paymentView, client):
        """
        Constructor that mainly connects buttons to handlers.

        :param paymentView: An instantiated PaymentView object.
        """
        self.paymentView = paymentView
        self.paymentView.tableScreen.clickedTableButton.connect(self.handleTableButtonClick)
        self.paymentView.paymentScreen.clickedBackButton.connect(self.handleBackButtonClick)
        self.paymentView.paymentScreen.clickedPayButton.connect(self.handlePayButtonClick)
        self.paymentView.paymentScreen.clickedPrintButton.connect(self.handlePrintButtonClick)
        self.client = client

    def handlePrintButtonClick(self):
        print("You've clicked the print button")

    def handlePayButtonClick(self):
        """
        Event handler that sends the value in the payment field to the server.
        """
        paid = self.paymentView.paymentScreen.paymentField.getValue()
#        self.client.sendPayment(paid)
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
        fieldFormat = "{:.2f}"

        self.paymentView.displayPaymentScreen(tableNumber)

        # Fetches the total bill from the server and then displays it
        total = 111
#        total = float(self.client.requestTotalBill(tableNumber))
        totalFormatted = fieldFormat.format(total)
        self.paymentView.paymentScreen.setTotalFieldValue(totalFormatted)

        # Calculates the change locally and then displays it
        paid = float(self.paymentView.paymentScreen.paidField.getValue())
        change = paid - total
        changeFormatted = fieldFormat.format(change)
        self.paymentView.paymentScreen.setChangeFieldValue(changeFormatted)


def _getRelativePath(*args):
    """
    Gets the relative path to a file.
    (Cross-platform and cross-script compatible)

    :param *args: The relative path to the desired file from the script that
    calls this function (comma separated).
    :return: The absolute path to the desired file.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), *args))


def main():
    """
    Main entry point to run GUI.
    """
    MainController()

if __name__ == "__main__":
    main()

#def fixPluginBug():
#    """
#    Points PyQt to a .dll file that fixes the 'windows' missing plugin bug.
#    """
#    dirname = os.path.dirname(PyQt5.__file__)
#    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
#    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
