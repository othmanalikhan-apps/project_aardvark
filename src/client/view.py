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
    QStackedWidget, QMainWindow, QScrollArea)
from PyQt5.QtGui import (
    QFont,
    QPixmap)
from PyQt5.QtCore import (
    Qt
)
from src.client.model import Client


class TabOrder(QTabWidget):
    pass

class TabBook(QTabWidget):
    pass

class TabPay(QTabWidget):
    pass




class TabHelp(QTabWidget):

    pass






class SplashScreen(QWidget):
    """
    A simple splash/starting screen
    """

    def __init__(self):
        """
        Loads an image, constructs a title and a button.
        """
        super().__init__()
        self.setWindowTitle("Team Aardvark")
        self.setFixedSize(300, 600)
        self.mainLayout = QVBoxLayout()

        self.mainLayout.addStretch(1)
        self.loadImage()
        self.createTitle()
        self.createNextButton()
        self.mainLayout.addStretch(1)

        self.setLayout(self.mainLayout)

    def loadImage(self):
        """
        Loads and displays the startup image.
        """
        path = _getRelativePath('..', '..', 'asset', 'logo.png')
        pixMap = QPixmap(path)
        pixMap = pixMap.scaled(500, 500, Qt.KeepAspectRatio)
        image = QLabel()
        image.setPixmap(pixMap)
        self.mainLayout.addWidget(image)

    def createTitle(self):
        """
        Creates a title label to be displayed on the splash screen.
        """
        titleFont = QFont("", 30, QFont.Bold, False)
        subtitleFont = QFont("", 8, QFont.Bold, False)
        titleLayout = QHBoxLayout()
        subtitleLayout = QHBoxLayout()

        title = QLabel()
        title.setText("Team Aardvark")
        title.setFont(titleFont)

        subtitle = QLabel()
        subtitle.setText("Serving With Hospitality")
        subtitle.setFont(subtitleFont)

        titleLayout.addStretch(1)
        titleLayout.addWidget(title)
        titleLayout.addStretch(1)

        subtitleLayout.addStretch(1)
        subtitleLayout.addWidget(subtitle)
        subtitleLayout.addStretch(1)

        self.mainLayout.addLayout(titleLayout)
        self.mainLayout.addLayout(subtitleLayout)

    def createNextButton(self):
        """
        Creates the next button to proceed to the next screen.
        """
        font = QFont("", 6, QFont.Bold, True)

        self.nextButton = QPushButton("Continue")
        self.nextButton.setFont(font)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.nextButton)


class TabMenu(QTabWidget):
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

        self.mainLayout = QHBoxLayout()
        self.nameLayout = QVBoxLayout()
        self.descLayout = QVBoxLayout()
        self.priceLayout = QVBoxLayout()

        self.menu = menu
        self.createGUI()

        self.mainLayout.addLayout(self.nameLayout)
        self.mainLayout.addStretch(1)
        self.mainLayout.addLayout(self.descLayout)
        self.mainLayout.addStretch(3)
        self.mainLayout.addLayout(self.priceLayout)
        self.setLayout(self.mainLayout)

    def createGUI(self):
        """
        Creates all the GUI components for the food entries in the tab.
        """
        foodType = self.menu.categorizeFood()

        typeNames = ["starter", "main course", "dessert", "beverage"]


        for type in typeNames:
            self.createTitle(type)
            for food in foodType[type]:
                self.createFoodPrices(food)
                self.createFoodDescription(food)
                self.createFoodNames(food)

    def createFoodNames(self, food):
        """
        Creates the food names on the vertical left hand-side of the tab.
        """
        font = QFont()
        font.setBold(True)
        font.setItalic(True)

        label = QLabel()
        label.setText(food.name)
        label.setFont(font)

        self.nameLayout.addWidget(label)

    def createFoodDescription(self, food):
        """
        Creates a text area where the food details will be stored.
        """
        class DescriptionLabel(QLabel):
            """
            Inner class for improved GUI scaling (dynamic text wrapping).
            """
            def resizeEvent(self, resizeEvent):
                self.setFixedWidth(self.window().width()*0.5)

        layout = QHBoxLayout()
        font = QFont()

        label = DescriptionLabel()
        label.setAlignment(Qt.AlignCenter)
        label.setText(food.description)
        label.setFont(font)
        label.setWordWrap(True)

        layout.addWidget(label)
        self.descLayout.addLayout(layout)

    def createFoodPrices(self, food):
        """
        Creates the prices on the vertical right hand-side of the tab.
        """
        template = "{:.2f} GBP"
        font = QFont()

        label = QLabel()
        label.setText(template.format(food.price))
        label.setFont(font)

        self.priceLayout.addWidget(label)

    def createTitle(self, type):
        """
        Creates a title for each type of food (e.g. starter, desserts, etc).
        """
        font = QFont("Arial", 20, QFont.Bold, False)
        dummyFont = QFont("Arial", 12, QFont.Bold, False)

        dummyLabelA = QLabel()
        dummyLabelA.setFont(dummyFont)
        dummyLabelB = QLabel()
        dummyLabelB.setFont(dummyFont)

        label = QLabel()
        label.setText(type.title())
        label.setFont(font)

        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(label)
        layout.addStretch(1)

        self.nameLayout.addWidget(dummyLabelA)
        self.descLayout.addLayout(layout)
        self.priceLayout.addWidget(dummyLabelB)









    def createButtons(self):
        """
        Create buttons.
        """
#        self.label = QLabel(self)
#        layout = QVBoxLayout(self)
#        layout.addWidget(self.label)
#        layout.addWidget(self.textArea)
#        layout.addWidget(self.button)

        self.button = QPushButton("Search", self)
        self.button.clicked.connect(self.handleSearchButton)
        self.textArea = QTextEdit(self)

    def handleSearchButton(self):
        """
        """
        name = self.textArea.toPlainText()

        client = Client()
        bookingRef = client.fetchBookingRef(name)

        self.label.setText(bookingRef)


class MainTab(QTabWidget):
    """
    View class of the MVC pattern. Responsible for displaying the GUI.
    """

    def __init__(self, serverSocket):
        """
        Main tab widget that constructs the client GUI.
        """
        super().__init__()
        self.setWindowTitle("Team Aardvark")
        self.setMinimumSize(1024, 600)
        self.mainLayout = QHBoxLayout()
        self.scrollArea = QScrollArea()

        self.client = Client(serverSocket)

        self.createTabs()
        self.tabs.addTab(self.tabMenu, "Menu")
        self.tabs.addTab(self.tabOrder, "Order")
        self.tabs.addTab(self.tabBook, "Booking")
        self.tabs.addTab(self.tabPay, "Payment")
        self.tabs.addTab(self.tabHelp, "Help")

        self.scrollArea.setWidget(self.tabs)
        self.scrollArea.setWidgetResizable(True)
        self.mainLayout.addWidget(self.scrollArea)
        self.setLayout(self.mainLayout)

    def createTabs(self):
        """
        Creates tabs.
        """
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(2)

        self.tabOrder = TabOrder()
        self.tabMenu = TabMenu(self.client.requestMenu())
        self.tabBook = TabBook()
        self.tabPay = TabPay()
        self.tabHelp = TabHelp()


def getStyle():
    """
    Attempts to return a preferred style. If not available, returns a default
    os style.
    :return: A style.
    """
    prefStyle = ["Windows"]
    defaultStyle = QStyleFactory.keys()[0]

    prefStyle = [style for style in prefStyle if style in QStyleFactory.keys()]
    prefStyle.append(defaultStyle)

    return prefStyle[0]

def getSocket():
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

def _getRelativePath(*args):
    """
    Gets the relative path to a file.
    (Cross-platform and cross-script compatible)

    :param *args: The relative path to the desired file from the script that
    calls this function (comma separated).
    :return: The absolute path to the desired file.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), *args))
