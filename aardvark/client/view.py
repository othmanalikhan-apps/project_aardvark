"""
View module of the MVC pattern of the client GUI.

As such, this module contains the actual PyQt5 GUI code that the
client will view.

In summary, the GUI is more or less built from multiple tab widgets which
are all then added to a single main widget that is displayed.
"""

__docformat__ = 'reStructuredText'

import os

from collections import OrderedDict

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QTabWidget,
    QStackedWidget, QMainWindow, QScrollArea, QSizePolicy, QLineEdit, QFrame,
    QDesktopWidget, QFormLayout, QDateEdit, QComboBox,
    QDialog, QMessageBox)
from PyQt5.QtGui import (
    QFont, QPixmap, QIcon
)
from PyQt5.QtCore import (
    Qt, pyqtSignal, QDate
)


class BookingView(QWidget):
    """
    Responsible for displaying the booking tab.
    """

    # customer's name, email, phone and booking's date, time, table, size
    clickedBookingButton = pyqtSignal(str, str, str, object, str, str, str)
    clickedDateEdit = pyqtSignal()
    clickedTimeField = pyqtSignal()
    clickedTableField = pyqtSignal()
    clickedSizeField = pyqtSignal()

    def __init__(self):
        """
        Constructs the booking tab.
        """
        super().__init__()
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)
        mainLayout.setAlignment(Qt.AlignCenter)

        # Add title
        self.mainTitleLayout = self.createTitleLayout()
        mainLayout.addLayout(self.mainTitleLayout)

        # Add image
        self.mainImage = self.createImageLayout()
        mainLayout.addLayout(self.mainImage)
        mainLayout.addSpacing(20)

        # Add forms for customer and booking details
        formsLayout = QHBoxLayout()
        formsLayout.setAlignment(Qt.AlignCenter)

        customerDetailsForm = self.createCustomerDetailsLayout()
        bookingDetailsForm = self.createBookingDetailsLayout()

        formsLayout.addStretch(1)
        formsLayout.addLayout(customerDetailsForm)
        formsLayout.addStretch(1)
        formsLayout.addLayout(bookingDetailsForm)
        formsLayout.addStretch(1)

        # Add both forms to main layout
        mainLayout.addLayout(formsLayout)
        mainLayout.addSpacing(20)

        # Create a booking status layout that contains the booking button
        # and reference number
        bookingStatusLayout = self.createBookingStatusLayout()
        mainLayout.addStretch(2)
        mainLayout.addLayout(bookingStatusLayout)
        mainLayout.addStretch(1)

    def createBookingStatusLayout(self):
        """
        Creates a layout containing the booking button and label which
        displays the reference number.

        :return: The booking status layout.
        """
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        bookingButton = self.createBookingButton()
        self.bookingStatusLabel = self.createBookingStatusLabel()
        layout.addStretch(1)
        layout.addWidget(bookingButton)
        layout.addStretch(2)
        layout.addWidget(self.bookingStatusLabel)
        layout.addStretch(1)
        return layout

    def createCustomerDetailsLayout(self):
        """
        Creates a layout containing name, email and phone number fields

        :return: The customer details layout.
        """
        layout = QFormLayout()
        layout.setFormAlignment(Qt.AlignCenter)
        layout.setLabelAlignment(Qt.AlignCenter)
        layout.setVerticalSpacing(20)

        self.nameField = QLineEdit()
        self.nameField.setMinimumWidth(300)
        layout.addRow("Name: ", self.nameField)

        self.emailField = QLineEdit()
        self.emailField.setMinimumWidth(300)
        layout.addRow("Email: ", self.emailField)

        self.phoneField = QLineEdit()
        self.phoneField.setMinimumWidth(300)
        layout.addRow("Phone: ", self.phoneField)
        return layout

    def createBookingDetailsLayout(self):
        """
        Creates a layout containing date, time, table and size fields.
        The date field implements a calendar widget allowing user to select
        date from a calendar.

        :return: The booking details layout.
        """
        layout = QFormLayout()
        layout.setFormAlignment(Qt.AlignCenter)
        layout.setLabelAlignment(Qt.AlignCenter)
        layout.setVerticalSpacing(20)

        self.dateField = QDateEdit(QDate.currentDate())
        self.dateField.setMinimumDate(QDate.currentDate())
        self.dateField.setCalendarPopup(True)
        self.dateField.setMinimumWidth(100)
        self.dateField.dateChanged.connect(lambda isClicked:
                                           self.clickedDateEdit.emit())
        layout.addRow("Date: ", self.dateField)

        self.timeField = QComboBox()
        self.timeField.setMinimumWidth(100)
        self.timeField.setDisabled(True)
        self.timeField.activated.connect(lambda isClicked:
                                         self.clickedTimeField.emit())
        layout.addRow("Time: ", self.timeField)

        self.sizeField = QComboBox()
        self.sizeField.setMinimumWidth(100)
        self.sizeField.setDisabled(True)
        self.sizeField.activated.connect(lambda isClicked:
                                                   self.clickedSizeField.emit())
        layout.addRow("Size: ", self.sizeField)

        self.tableField = QComboBox()
        self.tableField.setMinimumWidth(100)
        self.tableField.setDisabled(True)
        self.tableField.activated.connect(lambda isClicked:
                                          self.clickedTableField.emit())
        layout.addRow("Table: ", self.tableField)
        return layout

    def createImageLayout(self):
        """
        Creates a layout containing an image with a black border

        :return: The layout of the image.
        """
        layout = QHBoxLayout()
        imagePath = _getRelativePath('..', '..', 'asset', 'floor_plan.jpg')
        pixMap = QPixmap(imagePath)

        image = QLabel()
        image.setAlignment(Qt.AlignCenter)
        image.setStyleSheet("border: 2px solid black");
        image.setPixmap(pixMap)
        image.setFixedSize(600, 400)
        image.setScaledContents(True)
        layout.addWidget(image)
        return layout

    def createTitleLayout(self):
        """
        Creates a title displaying the number of the table.

        :return: The layout of the title.
        """
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        title = QLabel("Booking")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 20, QFont.Bold, False))
        layout.addWidget(title)
        return layout

    def createBookingButton(self):
        """
        Create a button that emits a clickedBookingButton signal when clicked.

        :return: The booking button.
        """
        bookingButton = QPushButton("Make Booking")
        bookingButton.setFont(QFont("", 14, QFont.Bold, False))
        # Emit a signal containing customer's name, email, phone and the
        # booking date, time, table entered in the fields when clicked
        bookingButton.clicked.connect(
            lambda isClicked: self.clickedBookingButton.emit(
            self.getCustomerName(),
            self.getCustomerEmail(),
            self.getCustomerPhone(),
            self.getBookingDate(),
            self.getBookingTime(),
            self.getBookingTable(),
            self.getBookingSize()
        ))
        bookingButton.setFixedSize(150, 50)
        return bookingButton

    def createBookingStatusLabel(self):
        """
        Creates the label used for displaying the success of a booking
        and the reference number

        :return: The booking status label.
        """
        label = QLabel("Reference #329382")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("", 16, QFont.Bold, True))
        return label

    def showEmptyFieldsPopup(self):
        """
        Displays a message box that notifies the user to
        fill in missing booking details.
        """
        text = "No field can be left undone..."
        self._generatePopup(text).show()

    def showInvalidEmailPopup(self):
        """
        Displays a message box that notifies the user to
        rectify the incorrect email entered.
        """
        text = "The email you entered is... INVALID!"
        self._generatePopup(text).show()

    def showInvalidPhonePopup(self):
        """
        Displays a message box that notifies the user to
        rectify the incorrect phone number entered.
        """
        text = "What kind of a phone number is that?"
        self._generatePopup(text).show()

    def _generatePopup(self, messageText):
        """
        Creates and initializes a standard QMessageBox.

        :param messageText: The text that the message box should display.
        :return: QMessageBox.
        """
        messageBox = QMessageBox(self)
        messageBox.setIcon(QMessageBox.Information)
        messageBox.setText(messageText)
        messageBox.setWindowTitle("Error")
        return messageBox

    def setBookingStatusText(self, text):
        """
        Sets the message to be displayed after completing the booking.

        :param text: message to be displayed on the label.
        """
        template = "Reference: #{}"
        self.bookingStatusLabel.setText(template.format(text))

    def getCustomerName(self):
        return self.nameField.text()

    def getCustomerEmail(self):
        return self.emailField.text()

    def getCustomerPhone(self):
        return self.phoneField.text()

    def getBookingDate(self):
        return self.dateField.date().toString("yyyy-MM-dd")

    def getBookingTable(self):
        return self.tableField.currentText()

    def getBookingTime(self):
        return self.timeField.currentText()

    def getBookingSize(self):
        return self.sizeField.currentText()


class OrderView(QStackedWidget):
    """
    Responsible for displaying the order tab.
    """

    def __init__(self, menu, tables):
        """
        Constructs the order tab.
        """
        super().__init__()
        # First widget where all tables are displayed.
        self.tableScreen = TableScreen(tables)
        self.tableScroll = QScrollArea()
        self.tableScroll.setWidget(self.tableScreen)
        self.tableScroll.setWidgetResizable(True)
        self.addWidget(self.tableScroll)

        # Second widget where order information for a particular table
        # is displayed
        self.orderScreen = OrderScreen(menu)
        self.orderScroll = QScrollArea()
        self.orderScroll.setWidget(self.orderScreen)
        self.orderScroll.setWidgetResizable(True)
        self.addWidget(self.orderScroll)

        # Set the table screen as the default
        self.setCurrentWidget(self.tableScroll)

    def displayTableScreen(self):
        """
        Sets the current widget to the table screen.
        """
        self.setCurrentWidget(self.tableScroll)

    def displayOrderScreen(self, tableNumber):
        """
        Sets the current widget to the order screen.

        :param tableNumber: The number of the table.
        """
        self.setCurrentWidget(self.orderScroll)
        self.orderScreen.setTableNumber(tableNumber)


class OrderScreen(QWidget):
    """
    Displays all the items on the menu that can be ordered as buttons.
    Clicking on an item adds it to the ordered items section.
    """
    clickedFoodButton = pyqtSignal(str)
    clickedSubtractButton = pyqtSignal(str)
    clickedAddButton = pyqtSignal(str)
    clickedSubmitButton = pyqtSignal()
    clickedBackButton = pyqtSignal()

    def __init__(self, menu):
        """
        Constructs the order screen which consists of titles of the food
        types, followed by buttons representing the food.
        Also, the end of the screen contains food items queued into the
        order basket.

        :param menu: An instantiated menu object.
        """
        super().__init__()
        mainLayout = QVBoxLayout()
        mainLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(mainLayout)

        # Get the food types and create a title for each type
        # Then create an entry for each of the foods within the food type
        foodType = menu.categorizeFood()

        for type in menu.getFoodTypes():
            # Create a title for each food type
            title = self.createTitle(type.title())
            titleLayout = QHBoxLayout()
            titleLayout.setAlignment(Qt.AlignCenter)
            titleLayout.addWidget(title)
            mainLayout.addLayout(titleLayout)

            # Group food buttons in rows
            rowLayout = QHBoxLayout()
            for food in foodType[type]:
                foodButton = self.createFoodButton(food.name)
                rowLayout.addWidget(foodButton)

            # Add row to main layout
            mainLayout.addLayout(rowLayout)
            mainLayout.addSpacing(20)

        # Ordered items section
        self.orderedItemsTitle = self.createTitle("Ordered Items")
        orderedItemsTitleLayout = QHBoxLayout()
        orderedItemsTitleLayout.setAlignment(Qt.AlignCenter)
        orderedItemsTitleLayout.addWidget(self.orderedItemsTitle)
        mainLayout.addLayout(orderedItemsTitleLayout)

        self.orderedItemsLayout = QVBoxLayout()
        mainLayout.addLayout(self.orderedItemsLayout)

        # Navigation section at end of page
        submitButton = self.createSubmitButton()
        backButton = self.createBackButton()
        navigationLayout = QHBoxLayout()
        navigationLayout.setAlignment(Qt.AlignCenter)
        navigationLayout.addWidget(backButton)
        navigationLayout.addSpacing(20)
        navigationLayout.addWidget(submitButton)
        mainLayout.addLayout(navigationLayout)

    def displayOrderedItems(self, orderedItems):
        """
        Updates the ordered items section displaying their quantity
        and description.

        :param orderedItems: An ordered dictionary containing the names of
        the food items and their quantities.
        """
        # Remove all items from previous display
        self.clearLayout(self.orderedItemsLayout)

        for (itemName, quantity) in orderedItems.items():
            # Create label to display the quantity
            layout = QHBoxLayout()
            quantityLabel = QLabel("{}x".format(quantity))
            quantityLabel.setFont(QFont("", 10, QFont.Bold, True))
            quantityLabel.setMaximumWidth(20)
            layout.addWidget(quantityLabel)
            layout.addSpacing(10)

            # Create label to display the name
            nameLabel = QLabel(itemName)
            nameLabel.setFont(QFont("", 10, QFont.StyleItalic, True))
            layout.addWidget(nameLabel)

            # Create the add and subtract button to remove quantity
            subtractButton = self.createSubtractButton(itemName)
            addButton = self.createAddButton(itemName)
            layout.addWidget(subtractButton)
            layout.addWidget(addButton)

            # Add all the combined widgets to the orderItemsLayout
            self.orderedItemsLayout.addLayout(layout)

    def createFoodButton(self, text):
        """
        Create a label on top of a button so that we can have multi-line text
        on a button. By default, QPushButton displays text on a single line.

        :param: The text string to be displayed on the button.
        :return: The food button.
        """
        button = QPushButton()
        button.setFixedSize(100, 100)
        button.setLayout(QVBoxLayout())

        label = QLabel(button)
        label.setText(text.title())
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 10, QFont.Normal, True))
        label.setMouseTracking(False)
        label.setWordWrap(True)
        label.setTextInteractionFlags(Qt.NoTextInteraction)

        button.layout().addWidget(label)

        # Emit a signal when the button is pressed with the button's text as
        # the argument
        button.clicked.connect(lambda isClicked, foodName=label.text():
                               self.clickedFoodButton.emit(foodName))
        return button

    def createSubtractButton(self, foodName):
        """
        Creates a subtract button corresponding to an item name in the
        ordered items basket.

        :param: The name of the food the button corresponds to.
        :return: The subtract button.
        """
        button = QPushButton("-")
        button.setFixedSize(20, 20)
        button.setLayout(QVBoxLayout())

        # Emit a signal when the button is pressed with the button's text as
        # the argument
        button.clicked.connect(lambda isClicked:
                               self.clickedSubtractButton.emit(foodName))
        return button

    def createAddButton(self, foodName):
        """
        Creates an add button corresponding to an item name in the
        ordered items basket.

        :param foodName: The name of the food the button corresponds to.
        :return: The add button.
        """
        button = QPushButton("+")
        button.setFixedSize(20, 20)
        button.setLayout(QVBoxLayout())

        # Emit a signal when the button is pressed with the button's text as
        # the argument
        button.clicked.connect(lambda isClicked:
                               self.clickedAddButton.emit(foodName))
        return button

    def createSubmitButton(self):
        """
        Creates the submit button.

        :return: The submit button.
        """
        button = QPushButton("Submit Order")
        button.setMaximumWidth(500)
        button.setMinimumHeight(20)
        button.clicked.connect(lambda isClicked: self.clickedSubmitButton.emit())
        return button

    def createBackButton(self):
        """
        Creates a button that sends user to previous screen.

        :return: The back button as a QPushButton.
        """
        button = QPushButton("Back")
        button.setMaximumWidth(500)
        button.setMinimumHeight(20)
        button.clicked.connect(lambda isClicked: self.clickedBackButton.emit())
        return button

    def createTitle(self, text):
        """
        Creates a title for each type of food (e.g. starter, desserts, etc).

        :param text: The string text of the title.
        :return: The title as a QLabel.
        """
        title = QLabel(text)
        title.setFont(QFont("Arial", 20, QFont.Bold, False))
        title.setAlignment(Qt.AlignCenter)
        return title

    def clearLayout(self, layout):
        """
        Clears all the widgets within a layout.
        """
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def setTableNumber(self, tableNumber):
        """
        Sets the ordered items title to the given table number.
        """
        self.orderedItemsTitle.setText("Ordered Items: Table {}"
                                       .format(tableNumber))

    def showFailPopup(self):
        """
        Displays a message box that notifies the user that the order has not
        been submitted successfully.
        """
        text = "Ordered could not be submitted successfully!"
        self._generatePopup(text).show()

    def showSuccessPopup(self):
        """
        Displays a message box that notifies the user that the order has been
        submitted successfully.
        """
        text = "Ordered submitted successfully!"
        self._generatePopup(text).show()

    def _generatePopup(self, messageText):
        """
        Creates and initializes a standard QMessageBox.

        :param messageText: The text that the message box should display.
        :return: QMessageBox.
        """
        messageBox = QMessageBox(self)
        messageBox.setIcon(QMessageBox.Information)
        messageBox.setText(messageText)
        messageBox.setWindowTitle("Fabulous!")
        return messageBox


class PaymentView(QStackedWidget):
    """
    Responsible for displaying the payment tab.
    """

    def __init__(self, tables):
        """
        Constructs the payment tab.

        :param tables: The total number of tables in the restaurant.
        """
        super().__init__()
        # First widget where all tables are displayed.
        self.tableScreen = TableScreen(tables)
        self.tableScroll = QScrollArea()
        self.tableScroll.setWidget(self.tableScreen)
        self.tableScroll.setWidgetResizable(True)
        self.addWidget(self.tableScroll)

        # Second widget where payment information for a particular
        # table is displayed
        self.paymentScreen = PaymentScreen()
        self.addWidget(self.paymentScreen)

        # Set the table screen as the default
        self.setCurrentWidget(self.tableScroll)

    def displayTableScreen(self):
        """
        Sets the current widget to the table screen.
        """
        self.setCurrentWidget(self.tableScroll)

    def displayPaymentScreen(self, tableNumber):
        """
        Sets the current widget to the payment screen.

        :param tableNumber: The number of the table.
        """
        self.setCurrentWidget(self.paymentScreen)
        self.paymentScreen.setTableNumber(tableNumber)


class PaymentScreen(QWidget):
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
        mainLayout.addStretch(1)

        # Create payment group and add it to main layout
        paymentLayout = self.createPaymentLayout()
        mainLayout.addLayout(paymentLayout)

        # Create calculation group and add it to main layout
        calculationsLayout = self.createCalculationsLayout()
        mainLayout.addLayout(calculationsLayout)
        mainLayout.addSpacing(20)
        mainLayout.addStretch(1)

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
        self.changeField = InputField("Change:", "00.00")
        calculationsLayout.addLayout(self.totalField.mainLayout)
        calculationsLayout.addLayout(self.paidField.mainLayout)
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
        self.paymentField.inputField.setReadOnly(False)
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
        backButton.setMaximumWidth(500)
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
        printButton.setFixedSize(500, 100)
        return printButton

    def setTableNumber(self, tableNumber):
        """
        Sets the title of the screen to the given table number.

        :param tableNumber: The number of the table.
        """
        self.title.setText("Payment: Table {}".format(tableNumber))

    def setTotalFieldValue(self, value):
        self.totalField.setValue(value)

    def setPaidFieldValue(self, value):
        self.paidField.setValue(value)

    def setChangeFieldValue(self, value):
        self.changeField.setValue(value)


class InputField:
    """
    Used by the PaymentScreen to simplify GUI designing.
    Combines a label and a line edit and stores their values.
    """

    def __init__(self, labelText, inputValue):
        """
        Constructs the InputField object.

        :param labelText: The name of the InputField.
        :param inputValue: The value to inserted into the line edit.
        """
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
        self.inputField.setReadOnly(True)
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


class TableScreen(QWidget):
    """
    Screen that displays the payment calculations options.
    """
    clickedTableButton = pyqtSignal(int)

    def __init__(self, tables):
        """
        Table Screen that is displayed within the PaymentView widget

        :param tables: The total number of tables in the restaurant.
        """
        super().__init__()
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        # Create title and add it to layout
        title = self.createTitle("Choose Table:")
        mainLayout.addWidget(title)
        mainLayout.addStretch(1)

        # Calculate total rows required for all buttons
        tablesPerRow = 5
        remainder = len(tables) % tablesPerRow
        totalRows = len(tables) // tablesPerRow

        # Add extra tables to complete row
        if remainder != 0:
            totalRows += 1

        # Create table buttons numbered from 1 to tables
        tableNumber = 0
        for row in range(totalRows):
            rowLayout = QHBoxLayout()
            rowLayout.addStretch(1)
            for col in range(tablesPerRow):

                # Adds a normal button if possible otherwise a blank button
                try:
                    tableButton = self.createTableButton(tables[tableNumber])
                    tableNumber += 1
                except IndexError:
                    tableButton = self.createBlankButton()

                rowLayout.addWidget(tableButton)
                rowLayout.addStretch(1)
            rowLayout.addStretch(1)
            mainLayout.addLayout(rowLayout)
            mainLayout.addSpacing(20)
        mainLayout.addStretch(1)

    def createTitle(self, text):
        """
        Creates a title with the given text.

        :param text: The string text of the title.
        :return: The title as a QLabel.
        """
        title = QLabel(text)
        title.setFont(QFont("", 20, QFont.Bold, False))
        return title

    def createTableButton(self, tableNumber):
        """
        Creates a 50x50 square button with the table number as the text

        :param tableNumber: The number of the table.
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

    def createBlankButton(self):
        """
        Creates a 50x50 square button blank button that doesn't do anything.
        Used to deal with GUI spacing issues.

        :return: The QPushButton with the table number on it.
        """
        button = QPushButton()
        button.setFixedSize(50, 50)
        button.setDisabled(True)
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

        :param food: An instantiated food object.
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
        priceLabel.setText(priceTemplate.format(float(food.price)))
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

        :param type: The type of the food object as a string.
        :return: The layout of the title.
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

        # Create a label for each of the title and description
        # and add it to main layout
        for (section, rawText) in self.generateHelpText().items():
            title = self.createTitle(section)
            description = self.createDescription(rawText)

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
        helpText = OrderedDict([
        ("Quick Guide", "MENU TAB: Displays the restaurant menu\n\n"
                           "ORDER TAB: Allows taking an order for a table\n\n"
                           "BOOKING TAB: Allows booking for a customer\n\n"
                           "PAYMENT TAB: Takes the payment of a customer\n\n"
                           "HELP TAB:  Displays some basic information"),
        ("About Us", "Team Aardvark is a group of Aardvarks that are "
                        "soon to undergo metamorphosis. Perhaps someday "
                        "we will be able to surpass the creature that "
                        "is also known as man. But for now, we wait "
                        "patiently until time is due."),
        ("Contact Us", "Email: ProgrammerK@gmail.com\n"
                          "Phone Number: 07472440699\n"
                          "Address: Team Aardvark, 20 Springfield, "
                          "Leeds, LS2 9NG, United Kingdom."),
        ("Legal", "WE ARE NOT RESPONSIBLE FOR ANY DAMAGE INCURRED BY THE "
                     "USE OF OUR PRODUCT NOR SHALL WE HOLD ANY LIABILITY. "
                     "ALL USE OF THE PRODUCT IS STRICTLY THE SOLE "
                     "RESPONSIBILITY OF THE USER.\n"
                     "REVERSE ENGINEERING AND MODIFICATION OF CODE IS ALLOWED"
                     " AS ALL THE CODE INVOLVED IN THE PROJECT IS CONSIDERED"
                     " OPEN SOURCE.")
        ])
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


class SplashView(QWidget):
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

    def __init__(self, menu, totalTables):
        """
        Main tab widget that constructs the client GUI.

        :param menu: An instantiated menu object.
        :param totalTables: The total number of tables in the restaurant.
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
        self.tabOrder = OrderView(menu, totalTables)
        self.tabMenu = MenuView(menu)
        self.tabBook = BookingView()
        self.tabPayment = PaymentView(totalTables)
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

        self.tabs.addTab(self.menuScroll, "Menu")
        self.tabs.addTab(self.tabOrder, "Order")
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

