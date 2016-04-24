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





class PaymentScreen(QWidget):
    """
    Screen that displays the payment calculations options.
    """

    def __init__(self, tableNumber):
        """
        Constructs the GUI for the payment screen.
        """
        super().__init__()
        self.mainLayout = QVBoxLayout()

        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QVBoxLayout()

        self.createTitleGUI(tableNumber)
        self.createSendGUI()
        self.createCalculationsGUI()
        self.createReceiptButtonGUI()
        self.createBackButtonGUI()

        self.topLayout.addLayout(self.leftLayout)
        self.topLayout.addLayout(self.rightLayout)

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

    def createTitleGUI(self, tableNumber):
        """
        Creates a title label for the tab.
        """
        font = QFont("", 20, QFont.Bold, False)
        layout = QHBoxLayout()

        title = QLabel()
        title.setText("Payment: Table {}".format(tableNumber))
        title.setFont(font)

        layout.addWidget(title)
        self.leftLayout.addLayout(layout)

    def createSendGUI(self):
        """
        Creates the section responsible for sending the payment.
        """
        labelFont = QFont("", 10, QFont.Normal, False)
        editFont = QFont("", 8, QFont.Bold, False)
        buttonFont = QFont("", 8, QFont.Bold, True)
        layout = QHBoxLayout()

        sendLabel = QLabel("Payment To Send:")
        sendLabel.setFont(labelFont)

        sendEdit = QLineEdit("00.00")
        sendEdit.setFont(editFont)

        sendButton = QPushButton("Send Payment")
        sendButton.setFont(buttonFont)

        layout.addWidget(sendLabel)
        layout.addStretch(1)
        layout.addWidget(sendEdit)
        layout.addStretch(1)
        layout.addWidget(sendButton)
        layout.addStretch(10)

        self.leftLayout.addStretch(1)
        self.leftLayout.addLayout(layout)
        self.leftLayout.addStretch(1)

    def createCalculationsGUI(self):
        """
        Creates the section responsible for payment calculations.
        """
        self.calculationsLayout = QHBoxLayout()

        self.createCalculationsLabel()
        self.createCalculationsEdit()
        self.leftLayout.addLayout(self.calculationsLayout)

    def createBackButtonGUI(self):
        """
        Creates a button to go back a screen.
        """
        buttonFont = QFont("", 8, QFont.Bold, True)
        backButton = QPushButton("Back")
        backButton.setFont(buttonFont)

        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(backButton)
        layout.addStretch(1)

        self.bottomLayout.addStretch(1)
        self.bottomLayout.addLayout(layout)

    def createReceiptButtonGUI(self):
        """
        Creates a button to print the receipt.
        """
        buttonFont = QFont("", 20, QFont.Bold, True)
        receiptButton = QPushButton("Print Receipt")
        receiptButton.setFont(buttonFont)
        receiptButton.setFixedSize(400, 100)

        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(receiptButton)
        layout.addStretch(1)

        self.bottomLayout.addStretch(1)
        self.bottomLayout.addLayout(layout)

    def createCalculationsLabel(self):
        """
        Creates the labels for the calculations section.
        """
        labelFont = QFont("", 10, QFont.Normal, False)
        labelList = ["Total:", "Paid:", "Remaining:", "Change:"]
        labelLayout = QVBoxLayout()

        for text in labelList:
            label = QLabel(text)
            label.setFont(labelFont)

            layout = QHBoxLayout()
            layout.addWidget(label)
            labelLayout.addLayout(layout)

        self.calculationsLayout.addLayout(labelLayout)

    def createCalculationsEdit(self):
        """
        Creates the line edit widgets for the calculations section.
        """
        editFont = QFont("", 8, QFont.Bold, False)
        editLayout = QVBoxLayout()

        totalEdit = QLineEdit()
        paidEdit = QLineEdit()
        remainingEdit = QLineEdit()
        changeEdit = QLineEdit()
        editList = [totalEdit, paidEdit, remainingEdit, changeEdit]

        for edit in editList:
            edit.setFont(editFont)
            edit.setText("00.00")
            edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            layout = QHBoxLayout()
            layout.addStretch(1)
            layout.addWidget(edit)
            layout.addStretch(2)
            editLayout.addLayout(layout)

        self.calculationsLayout.addLayout(editLayout)




class TableScreen(QWidget):
    """
    Screen that displays table numbers to be selected.
    """

    def __init__(self, totalTables):
        """
        Constructs a button for each table in a grid like fashion.
        """
        super().__init__()
        self.totalTables = totalTables
        self.mainLayout = QVBoxLayout()

        self.createTitle()
        self.createButtons()
        self.setLayout(self.mainLayout)

    def createButtons(self):
        """
        Creates the all sections which consists of a title and a paragraph.
        """
        font = QFont("", 14, QFont.Normal, True)
        buttonsLayout = QVBoxLayout()

        tableNum = 0
        tablesPerRow = 10
        remainder = self.totalTables % tablesPerRow

        if remainder == 0:
            totalRows = self.totalTables // tablesPerRow
        else:
            totalRows = (self.totalTables // tablesPerRow) + 1

        for row in range(totalRows):
            rowLayout = QHBoxLayout()
            rowLayout.addStretch(1)
            for col in range(1, tablesPerRow+1):
                tableNum += 1
                button = QPushButton(str(tableNum))
                button.setFixedSize(50, 50)
                button.setFont(font)
                button.clicked.connect(self.handleButton(button))

                rowLayout.addWidget(button)
                rowLayout.addStretch(1)

            buttonsLayout.addLayout(rowLayout)
            buttonsLayout.addStretch(1)


        self.mainLayout.addLayout(buttonsLayout)

    def handleButton(self, button):
        """
        The button handler for each button.
        :return: The table number of the button.
        """
        def printButtonText():
#            print(button.text())
            self.chosenOne = button.text()

        return printButtonText

    def createTitle(self):
        """
        Creates a title label for the tab.
        """
        font = QFont("", 20, QFont.Bold, False)
        layout = QHBoxLayout()

        title = QLabel()
        title.setText("Choose Table:")
        title.setFont(font)

        layout.addWidget(title)
        layout.addStretch(1)
        self.mainLayout.addLayout(layout)
        self.mainLayout.addSpacing(20)












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
        self.tabPayment = PaymentView()
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
        self.tabs.addTab(self.tabPayment, "Payment")
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

