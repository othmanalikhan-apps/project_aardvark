"""
View module of the MVC pattern of the client GUI.

As such, this module contains the actual PyQt5 GUI code that the
client will view.

In summary, the GUI is built from multiple tab widgets which are all then
added to a single main widget that is displayed.
"""
from PyQt5.QtCore import Qt
from PyQt5.uic.properties import QtCore

__docformat__ = 'reStructuredText'


import os
import configparser

from src.client.model import Client

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QTextEdit, QTabWidget, QStyleFactory
)
from PyQt5.QtGui import (
    QFont
)




class TabOrder(QTabWidget):
    pass

class TabBook(QTabWidget):
    pass

class TabPay(QTabWidget):
    pass

class TabHelp(QTabWidget):
    pass

class SplashScreen():
    pass












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
        self.show()

    @staticmethod
    def categorizeFood(menu):
        """
        Separates the food into types (e.g. main course, desserts, etc).

        :param menu: A menu object that contains the food items.
        :return: A dictionary that maps food type to a food object.
        """
        foodType = {}

        for food in menu.items:
            if food.type not in foodType.keys():
                foodType[food.type] = []
            foodType[food.type].append(food)

        return foodType

    def createGUI(self):
        """
        Creates all the GUI components for the food entries in the tab.
        """
        foodType = self.categorizeFood(self.menu)
        typeNames = ["starter", "main course", "dessert", "beverage"]

        for type in typeNames:
            self.createTitle(type)
            pass
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

        dummyLabel = QLabel()
        dummyLabel.setFont(font)

        label = QLabel()
        label.setText(type.title())
        label.setFont(font)

        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(label)
        layout.addStretch(1)

        self.nameLayout.addWidget(dummyLabel)
        self.descLayout.addLayout(layout)
        self.priceLayout.addWidget(dummyLabel)









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


class View(QWidget):
    """
    View class of the MVC pattern. Responsible for displaying the GUI.
    """

    def __init__(self, serverSocket):
        """
        Main Widget that constructs the client GUI.
        """
        super().__init__()
        self.client = Client(serverSocket)

        self.createTabs()
        self.tabs.addTab(self.tabMenu, "Menu")
        self.tabs.addTab(self.tabOrder, "Order")
        self.tabs.addTab(self.tabBook, "Booking")
        self.tabs.addTab(self.tabPay, "Payment")
        self.tabs.addTab(self.tabHelp, "Help")

    def createTabs(self):
        """
        Creates tabs.
        """
        self.tabs = QTabWidget()
        self.tabs.resize(640, 480)
        self.tabs.setWindowTitle("Team Aardvark")
        self.tabs.setTabPosition(2)

        menu = self.client.requestMenu()

        self.tabOrder = TabOrder()
        self.tabMenu = TabMenu(menu)
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
    path = os.path.join("..", "..", "settings.ini")
    if not os.path.exists(path):
        raise FileNotFoundError("Could not find the settings.ini file!")

    config = configparser.ConfigParser()
    config.read(path)
    return config.get("Network", "serversocket")


