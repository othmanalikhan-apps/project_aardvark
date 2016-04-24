"""
View module of the MVC pattern of the client GUI.

As such, this module contains the actual PyQt5 GUI code that the
client will view.

In summary, the GUI is more or less built from multiple tab widgets which
are all then added to a single main widget that is displayed.
"""

__docformat__ = 'reStructuredText'

import os
import configparser

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QTextEdit, QTabWidget, QStyleFactory,
    QStackedWidget, QMainWindow, QScrollArea, QSizePolicy, QLineEdit, QFrame,
    QDesktopWidget)
from PyQt5.QtGui import (
    QFont,
    QPixmap, QIcon)
from PyQt5.QtCore import (
    Qt,
    QObject, pyqtSignal)
from src.client.model import Client


class OrderView(QTabWidget):
    pass

class BookingView(QTabWidget):
    pass



class PaymentView(QTabWidget):
    """
    Responsible for displaying the payment tab of the GUI.
    """

    def __init__(self):
        """
        Constructs the payment tab of the GUI.
        """
        super().__init__()
        self.mainLayout = QVBoxLayout()
        self.mainWidget = QStackedWidget()

        tableScreen = TableScreen(255)
        self.paymentScreen = PaymentScreen(11)

        self.tableScrollScreen = QScrollArea()
        self.tableScrollScreen.setWidget(tableScreen)
        self.tableScrollScreen.setWidgetResizable(True)

        self.mainWidget.addWidget(self.tableScrollScreen)
        self.mainWidget.addWidget(self.paymentScreen)

#        self.mainWidget.setCurrentWidget(self.tableScrollScreen)
        self.mainWidget.setCurrentWidget(self.paymentScreen)

        self.mainLayout.addWidget(self.mainWidget)
        self.setLayout(self.mainLayout)


    def createTableScreen(self):
        """
        Creates the all sections which consists of a title and a paragraph.
        """
        self.titleFont = QFont("Arial", 20, QFont.Bold, False)
        self.descriptionFont = QFont("Arial", 10, QFont.Normal, False)

        for [section, description] in self.section:
            title = QLabel(section)
            title.setFont(self.titleFont)
            description = QLabel(description)
            description.setFont(self.descriptionFont)
            description.setWordWrap(True)

            layout = QVBoxLayout()
            layout.addStretch(1)
            layout.addWidget(title)
            layout.addWidget(description)
            layout.addStretch(1)

            self.mainLayout.addLayout(layout)






class PaymentScreen(QWidget, QObject):
    """
    Screen that displays the payment calculations options.
    """
    clickedBackButton = pyqtSignal()
    clickedPayButton = pyqtSignal()
    clickedPrintButton = pyqtSignal()

    def __init__(self):
        """
        Constructs the GUI for the payment screen.
        """
        super().__init__()
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(mainLayout)

        mainLayout.addStretch(1)

        # Create title and add it to main layout
        self.title = self.createTitle()
        mainLayout.addWidget(self.title)
        mainLayout.addSpacing(20)

        # Create payment group and add it to main layout
        paymentLayout = self.createPaymentLayout()
        mainLayout.addLayout(paymentLayout)

        # Create calculation group and add it to main layout
        calculationsLayout = self.createCalculationsLayout()
        mainLayout.addLayout(calculationsLayout)

        # Create print receipt button and add it to main layout
        self.printButton = self.createPrintButton()
        printButtonLayout = QHBoxLayout()
        printButtonLayout.addWidget(self.printButton)
        mainLayout.addLayout(printButtonLayout)

        # Create back button and add it to main layout
        self.backButton = self.createBackButton()
        backButtonLayout = QHBoxLayout()
        backButtonLayout.addWidget(self.backButton)
        mainLayout.addLayout(backButtonLayout)

        mainLayout.addStretch(2)

    def createCalculationsLayout(self):
        """
        Creates the layout where payment calculations occur.
        Namely, total bill, amount to pay, amount remaining, and change left
        fields are created.
        :return: The calculations layout.
        """
        calculationsLayout = QVBoxLayout()
        self.totalField = InputField("Total:", "00.00")
        self.paidField = InputField("Paid:", "00.00")
        self.remainingField = InputField("Remaining:", "00.00")
        self.changeField = InputField("Change:", "00.00")
        calculationsLayout.addLayout(self.totalField.mainLayout)
        calculationsLayout.addLayout(self.paidField.mainLayout)
        calculationsLayout.addLayout(self.remainingField.mainLayout)
        calculationsLayout.addLayout(self.changeField.mainLayout)
        calculationsLayout.addStretch(1)
        return calculationsLayout

    def createPaymentLayout(self):
        """
        Creates the layout where payment is sent.
        Namely, creates an input field to enter payment along with a button
        to send the payment.
        :return: The payment layout.
        """
        paymentLayout = QHBoxLayout()
        self.paymentField = InputField(" ", "00.00")
        self.payButton = self.createPayButton()
        paymentLayout.addStretch(2)
        paymentLayout.addLayout(self.paymentField.mainLayout)
        paymentLayout.addWidget(self.payButton)
        paymentLayout.addStretch(1)
        return paymentLayout

    def createTitle(self):
        """
        Creates a title displaying the table number.
        :return: The title as a QLabel.
        """
        title = QLabel("Payment: Table 1")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("", 20, QFont.Bold, False))
        return title

    def createPayButton(self):
        """
        Creates a button to submit the payment.
        :return: The payment button as a QPushButton.
        """
        payButton = QPushButton("Pay")
        payButton.setFont(QFont("", 8, QFont.Bold, True))
        payButton.clicked.connect(lambda x: self.clickedPayButton.emit())
        return payButton

    def createBackButton(self):
        """
        Creates a button that sends user to previous screen.
        :return: The back button as a QPushButton.
        """
        backButton = QPushButton("Back")
        backButton.setMaximumWidth(400)
        backButton.setFont(QFont("", 8, QFont.Bold, True))
        backButton.clicked.connect(lambda isClicked: self.clickedBackButton.emit())
        return backButton

    def createPrintButton(self):
        """
        Creates a button that prints the receipt for the user in a pop up
        dialog.
        :return: The receipt button as a QPushButton.
        """
        printButton = QPushButton("Print Receipt")
        printButton.setFont(QFont("", 20, QFont.Bold, True))
        printButton.clicked.connect(lambda isClicked: self.clickedPrintButton.emit())
        printButton.setFixedSize(400, 100)
        return printButton

    def setTableNumber(self, tableNumber):
        """
        Sets the title of the screen to the given table number.
        """
        self.title.setText("Payment: Table {}".format(tableNumber))

    def setTotalFieldValue(self, value):
        self.totalField.setValue(value)

    def setPaidFieldValue(self, value):
        self.paidField.setValue(value)

    def setRemainingFieldValue(self, value):
        self.remainingField.setValue(value)

    def setChangeFieldValue(self, value):
        self.changeField.setValue(value)


class InputField:
    """
    Used by the PaymentScreen to simplify GUI designing.
    Combine a label and a line edit and stores their values..
    """
    def __init__(self, labelText, inputValue):
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignCenter)

        self.mainLayout.addStretch(1)

        # Create the label
        self.label = QLabel(labelText)
        self.label.setMinimumWidth(200)
        self.label.setFont(QFont("", 10, QFont.Normal, False))
        self.mainLayout.addWidget(self.label)
        self.mainLayout.addStretch(1)

        # Create a currency format label
        self.currencyFormatLabel = QLabel("£")
        self.currencyFormatLabel.setMinimumWidth(10)
        self.currencyFormatLabel.setFont(QFont("", 10, QFont.Normal, False))
        self.mainLayout.addWidget(self.currencyFormatLabel)

        # Create the input field
        self.inputField = QLineEdit(inputValue)
        self.inputField.setMaximumWidth(200)
        self.inputField.setFont(QFont("", 8, QFont.Bold, False))
        self.mainLayout.addWidget(self.inputField)

        self.mainLayout.addStretch(1)

    def setValue(self, value):
        self.inputField.setText(str(value))

    def getValue(self):
        return self.inputField.text()

    def clearValue(self):
        """
        Sets the inputField to 00.00.
        """
        self.inputField.setText(str("00.00"))


class TableScreen(QWidget, QObject):
    """
    Screen that displays the payment calculations options.
    """
    clickedTableButton = pyqtSignal(int)

    def __init__(self, totalTables):
        """
        Table Screen that is displayed within the PaymentView widget
        """
        super().__init__()
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        # Create title and add it to layout
        title = self.createTitle("Choose Table:")
        mainLayout.addWidget(title)
        mainLayout.addStretch(1)

        # Calculate total rows required for all buttons
        tablesPerRow = 10
        remainder = totalTables % tablesPerRow
        totalRows = totalTables // tablesPerRow

        # Add extra tables to complete row
        if remainder != 0:
            totalRows += 1

        # Create table buttons numbered from 1 to totalTables
        tableNumber = 0
        for row in range(totalRows):
            rowLayout = QHBoxLayout()
            rowLayout.addStretch(1)
            for col in range(1, tablesPerRow + 1):
                tableNumber += 1
                tableButton = self.createTableButton(tableNumber)
                rowLayout.addWidget(tableButton)
                rowLayout.addStretch(1)
            rowLayout.addStretch(1)
            mainLayout.addLayout(rowLayout)

    def createTitle(self, text):
        """
        Creates a title with the given text.
        :return: The title as a QLabel.
        """
        title = QLabel(text)
        title.setFont(QFont("", 20, QFont.Bold, False))
        return title

    def createTableButton(self, tableNumber):
        """
        Creates a 50x50 square button with the table number as the text
        :return: The QPushButton with the table number on it.
        """
        button = QPushButton(str(tableNumber))
        button.setFixedSize(50, 50)
        button.setFont(QFont("", 14, QFont.Normal, True))
        # Emit a signal when the button is pressed with the button's
        # text as the argument
        button.clicked.connect(lambda isClicked, tableNumber=button.text():
                               self.clickedTableButton.emit(int(tableNumber)))
        return button


class MenuView(QWidget):
    """
    Responsible for displaying the menu tab of the GUI.
    """

    def __init__(self, menu):
        """
        Constructs the menu tab of the GUI.

        :param menu: A menu object which contains information about the
        food items available.
        """
        super().__init__()
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        foodType = menu.categorizeFood()
        typeNames = ["starter", "main course", "dessert", "beverage"]

        for type in typeNames:
            self.mainLayout.addLayout(self.createTitleLayout(type))
            for food in foodType[type]:
                self.mainLayout.addLayout(self.createFoodEntryLayout(food))

    def createFoodEntryLayout(self, food):
        """
        Creates a single food entry which consists of a name, description
        and a price.
        :return: The layout of the food entry.
        """
        nameFont = QFont("", 10, QFont.Bold, True)
        nameLabel = QLabel()
        nameLabel.setText(food.name)
        nameLabel.setAlignment(Qt.AlignLeft)
        nameLabel.setFont(nameFont)
        nameLabel.setWordWrap(True)
        nameLabel.setFixedWidth(200)

        descLabel = QLabel()
        descLabel.setText(food.description)
        descLabel.setAlignment(Qt.AlignLeft)
        descLabel.setWordWrap(True)
        descLabel.setSizePolicy(QSizePolicy.MinimumExpanding,
                                QSizePolicy.Preferred)

        priceTemplate = "{:.2f} GBP"
        priceLabel = QLabel()
        priceLabel.setText(priceTemplate.format(food.price))
        priceLabel.setAlignment(Qt.AlignRight)
        priceLabel.setFixedWidth(50)

        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(nameLabel)
        layout.addWidget(descLabel)
        layout.addWidget(priceLabel)
        return layout

    def createTitleLayout(self, type):
        """
        Creates a title for each type of food (e.g. starter, desserts, etc).
        """
        title = QLabel(type.title())
        title.setFont(QFont("Arial", 20, QFont.Bold, False))
        title.setAlignment(Qt.AlignCenter)
        layout = QHBoxLayout()
        layout.addWidget(title)
        return layout


class HelpView(QWidget):
    """
    Responsible for displaying the help tab of the GUI.
    """

    def __init__(self):
        """
        Constructs the help tab of the GUI.
        """
        super().__init__()
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        helpText = self.generateHelpText()

        # Determines the order in which the sections are displayed
        sections = ["Quick Guide", "About Us", "Contact Us", "Legal"]

        # Create a label for each of the title and description
        # and add it to main layout
        for section in sections:
            title = self.createTitle(section)
            description = self.createDescription(helpText[section])

            mainLayout.addStretch(1)
            mainLayout.addWidget(title)
            mainLayout.addWidget(description)
            mainLayout.addStretch(1)

    def generateHelpText(self):
        """
        Creates a dict which maps section title to section text for
        each section.
        :return: A dictionary which maps section title to section text.
        """
        helpText = {
            "Quick Guide": "MENU TAB: Displays the restaurant menu\n\n"
                           "ORDER TAB: Allows taking an order for a table\n\n"
                           "BOOKING TAB: Allows booking for a customer\n\n"
                           "PAYMENT TAB: Takes the payment of a customer\n\n"
                           "HELP TAB:  Displays some basic information",
            "About Us": "Team Aardvark is a group of Aardvarks that are "
                        "soon to undergo metamorphosis. Perhaps someday "
                        "we will be able to surpass the creature that "
                        "is also known as man. But for now, we wait "
                        "patiently until time is due.",
            "Contact Us": "Email: ProgrammerK@gmail.com\n"
                          "Phone Number: 07472440699\n"
                          "Address: Team Aardvark, 20 Springfield, "
                          "Leeds, LS2 9NG, United Kingdom.",
            "Legal": "WE ARE NOT RESPONSIBLE FOR ANY DAMAGE INCURRED BY THE "
                     "USE OF OUR PRODUCT NOR SHALL WE HOLD ANY LIABILITY. "
                     "ALL USE OF THE PRODUCT IS STRICTLY THE SOLE "
                     "RESPONSIBILITY OF THE USER.\n"
                     "REVERSE ENGINEERING AND MODIFICATION OF CODE IS ALLOWED"
                     " AS ALL THE CODE INVOLVED IN THE PROJECT IS CONSIDERED"
                     " OPEN SOURCE."
        }

        return helpText

    def createTitle(self, text):
        """
        Creates a QLabel for the title.
        :param text: The text of the title.
        :return: The title QLabel.
        """
        title = QLabel(text)
        title.setFont(QFont("Arial", 20, QFont.Bold, False))
        return title

    def createDescription(self, text):
        """
        Creates a QLabel for the description.
        :param text: The text of the description.
        :return: The description QLabel.
        """
        description = QLabel(text)
        description.setFont(QFont("Arial", 10, QFont.Normal, False))
        description.setWordWrap(True)
        return description


class SplashView(QWidget, QObject):
    """
    The first (starter) screen before entering the heart of the GUI.
    """
    clickedContinueButton = pyqtSignal()

    def __init__(self):
        """
        Creates an image, title, subtitle and a button.
        """
        super().__init__()
        self.setFixedSize(300, 600)
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(mainLayout)

        mainImage = self.createImage()
        titleLayout = self.createTitleLayout()
        subtitleLayout = self.createSubtitleLayout()
        continueButton = self.createContinueButton()

        mainLayout.addStretch(1)
        mainLayout.addWidget(mainImage)
        mainLayout.addStretch(1)
        mainLayout.addLayout(titleLayout)
        mainLayout.addLayout(subtitleLayout)
        mainLayout.addStretch(1)
        mainLayout.addWidget(continueButton)
        mainLayout.addStretch(2)

    def createImage(self):
        """
        Loads and displays the startup image.
        :return: A QLabel image.
        """
        path = _getRelativePath('..', '..', 'asset', 'logo.png')
        pixMap = QPixmap(path)
        pixMap = pixMap.scaled(500, 500, Qt.KeepAspectRatio)

        image = QLabel()
        image.setPixmap(pixMap)
        return image

    def createTitleLayout(self):
        """
        Creates a title label.
        :return: The title layout.
        """
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        title = QLabel("Team Aardvark")
        title.setFont(QFont("", 30, QFont.Bold, False))
        layout.addWidget(title)
        return layout

    def createSubtitleLayout(self):
        """
        Creates a subtitle label.
        :return: The subtitle layout.
        """
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        subtitle = QLabel("Serving With Hospitality")
        subtitle.setFont(QFont("", 8, QFont.Bold, False))
        layout.addWidget(subtitle)
        return layout

    def createContinueButton(self):
        """
        Creates the next button to proceed to the next screen.
        :return: The continue QPushButton.
        """
        button = QPushButton("Continue")
        button.clicked.connect(lambda isClicked:
                               self.clickedContinueButton.emit())
        button.setFont(QFont("", 6, QFont.Bold, True))
        return button


class MainView(QMainWindow):
    """
    View class of the MVC pattern. Responsible for displaying the GUI.
    """

    def __init__(self, menu):
        """
        Main tab widget that constructs the client GUI.
        """
        super().__init__()
        self.setCentralWidget(QStackedWidget())

        # Widgets to be added to the main window
        self.splash = SplashView()
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(2)

        # Set size, title and icon of main window
        self.initializeUI()

        # Create 5 widgets which will be used in 5 different tabs
#        self.tabOrder = OrderView(menu)
        self.tabMenu = MenuView(menu)
        self.tabBook = BookingView()
#        self.tabPayment = PaymentView()
        self.tabHelp = HelpView()

        # Wrap menu, help and book tabs in scroll widgets to allow scrolling
        self.menuScroll = QScrollArea()
        self.menuScroll.setWidget(self.tabMenu)
        self.menuScroll.setWidgetResizable(True)

        self.helpScroll = QScrollArea()
        self.helpScroll.setWidget(self.tabHelp)
        self.helpScroll.setWidgetResizable(True)

        self.bookScroll = QScrollArea()
        self.bookScroll.setWidget(self.tabBook)
        self.bookScroll.setWidgetResizable(True)

        # Hacky solution for adding a border/frame effect
#        self.scrollArea = QScrollArea()
#        self.scrollArea.setWidget(self.tabs)
#        self.scrollArea.setWidgetResizable(True)
#        self.setStyleSheet("border:1px solid rgb(0, 255, 0); ")

        self.tabs.addTab(self.menuScroll, "Menu")
#        self.tabs.addTab(self.tabOrder, "Order")
        self.tabs.addTab(self.bookScroll, "Booking")
#        self.tabs.addTab(self.tabPayment, "Payment")
        self.tabs.addTab(self.helpScroll, "Help")

        self.centralWidget().addWidget(self.splash)
        self.centralWidget().addWidget(self.tabs)
        self.displaySplash()
        self.show()

    def displaySplash(self):
        """
        Sets the current widget in the stack as the splash screen.
        """
        self.centralWidget().setCurrentWidget(self.splash)
        self.setMinimumSize(self.splash.size())
        self.setMaximumSize(self.splash.size())

    def displayTabs(self):
        """
        Sets the current widget in the stack as the tabbed widget
        and resizes the main window accordingly.
        """
        self.centralWidget().setCurrentWidget(self.tabs)
        self.setMinimumSize(1024, 600)
        screenGeometry = QDesktopWidget().screenGeometry()
        self.setMaximumSize(screenGeometry.width(), screenGeometry.height())

    def initializeUI(self):
        """
        Initializes the GUI UI which includes window title and status bar.
        """
        self.setWindowTitle("Team Aardvark")
        self.setWindowIcon(QIcon(QPixmap(1, 1)))
        self.statusBar().showMessage('Ready')
        self.centralWidget().setFrameStyle(QFrame.Plain | QFrame.Raised)
        self.centralWidget().setLineWidth(3)
        self.centralWidget().setMidLineWidth(3)
        self.centralWidget().setContentsMargins(-1, -1, -1, -1)


def _getRelativePath(*args):
    """
    Gets the relative path to a file.
    (Cross-platform and cross-script compatible)

    :param *args: The relative path to the desired file from the script that
    calls this function (comma separated).
    :return: The absolute path to the desired file.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), *args))

