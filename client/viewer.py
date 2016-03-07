"""
Courtesy of Stackoverflow:

http://stackoverflow.com/questions/19966056/
pyqt5-how-can-i-connect-a-qpushbutton-to-a-slot
"""

from model import Client

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QTextEdit, QTabWidget, QStyleFactory
)
from PyQt5.QtGui import ( QFont )

class TabOrder(QTabWidget):
    pass

class TabBook(QTabWidget):
    pass

class TabPay(QTabWidget):
    pass

class TabHelp(QTabWidget):
    pass


#TODO: fOOd is a tOOple

class TabMenu(QTabWidget):
    """
    The tab widget responsible for the menu section of the GUI.
    This involves displaying the menu on the screen.
    """

    def __init__(self, menu):
        """
        Constructs the menu tab of the GUI.
        :param menu: A list containing the information about the
        food items available.
        """
        super().__init__()

        self.mainLayout = QVBoxLayout()
        self.foodLayout = QVBoxLayout()


        foodInfo = self.categorizeFood(menu)
        self.createFoodEntries(foodInfo)

        self.foodLayout.addStretch(1)
        self.mainLayout.addLayout(self.foodLayout)
        self.setLayout(self.mainLayout)


    def categorizeFood(self, menu):
        """
        Separates the food into types (e.g. main course, desserts, etc).
        :return: A dictionary that maps food type to a list containing food
        information as a tuple. Thus of form form
        type:[(name, description, price)].
        """
        foodType = {}

        for (name, type, description, price) in menu:
            foodType[type] = []

        for (name, type, description, price) in menu:
            foodType[type].append((name, description, price))

        return foodType


    def createFoodEntries(self, foodType):
        """
        :param foodType: A list containing the information about the
        food items available.
        """
        for type in foodType.keys():
            self.createTitle(type)
            for (name, description, price) in foodType[type]:
                self.createTextArea(name, description, price)
#                self.createImageArea(name)


    def createTextArea(self, name, description, price):
        """
        Creates a text area where the food details will be stored.
        """
        self.layout = QHBoxLayout()

        fontName = QFont()
        fontName.setBold(True)

        fontDescr = QFont()
        fontName.setItalic(True)

        priceTemplate = "{:.2f} GBP"

        labelName = QLabel()
        labelDescr = QLabel()
        labelPrice = QLabel()

        labelName.setText(name)
        labelDescr.setText(description)
        labelPrice.setText(priceTemplate.format(price))

        labelName.setFont(fontName)
        labelDescr.setFont(fontDescr)
        labelDescr.setWordWrap(True)

#        label.setFrameStyle(6)

        self.layout.addWidget(labelName)
        self.layout.addStretch(1)
        self.layout.addWidget(labelDescr)
        self.layout.addStretch(1)
        self.layout.addWidget(labelPrice)
        self.foodLayout.addLayout(self.layout)
        self.foodLayout.addStretch(1)


    def createImageArea(self):
        """
        Creates an area where the food image will be stored.
        """
        pass

    def createTitle(self, type):
        """
        Creates a title for each type of food (e.g. starter, desserts, etc).
        """
        font = QFont("Arial", 20, QFont.Bold, False)

        label = QLabel()
        label.setText(type)
        label.setFont(font)

        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(label)
        layout.addStretch(1)

        self.foodLayout.addLayout(layout)


class Viewer(QWidget):

    def __init__(self):
        """
        Constructs the client GUI.
        """
        super().__init__()


#        client = Client("333")
#        client.fetchData()



        self.createTabs()

        self.tabs.addTab(self.tabMenu, "Menu")
        self.tabs.addTab(self.tabOrder, "Order")
        self.tabs.addTab(self.tabBook, "Booking")
        self.tabs.addTab(self.tabPay, "Payment")
        self.tabs.addTab(self.tabHelp, "Help")
        self.tabs.show()




    def createTabs(self):
        """
        Creates tabs.
        """
        self.tabs = QTabWidget()
        self.tabs.resize(640, 480)
        self.tabs.setWindowTitle("Team Aardvark")

        self.tabs.setTabPosition(2)


        descr1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " \
                 "Duis sit amet tempus enim. Sed scelerisque risus vitae dolor " \
                 "sodales viverra. Nam suscipit leo vel dolor semper, ut " \
                 "faucibus libero porttitor. Sed ut egestas leo. Phasellus " \
                 "in sollicitudin quam. Nullam sollicitudin posuere mauris " \
                 "et facilisis."

        descr2 = "Liquidify... My hopes and dreams... And let it but rot " \
                 "away... For I, have but hesitated... When travelling down " \
                 "the " \
                 "road... That diverges beyond the yellow horizon..."

        menu = {("Seaweed", "Breakfast", descr1, 10),
                ("Cabbage", "Breakfast", descr1, 10),
                ("Seaweed", "Breakfast", descr1, 10),
                ("Potato", "Lunch", descr1, 4),
                ("Apple", "Brunch", descr1, 4)}


        self.tabOrder = TabOrder()
        self.tabMenu = TabMenu(menu)
        self.tabBook = TabBook()
        self.tabPay = TabPay()
        self.tabHelp = TabHelp()


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


def main():
    """
    Runs the GUI.
    """
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Windows"))
#    print(QStyleFactory.keys())
    window = Viewer()

    sys.exit(app.exec_())


if __name__ == "__main__":

    import sys

    main()


