"""
the client side of the restaurant server-client system
"""

__docformat__ = 'reStructuredText'

import unittest
import requests

from unittest.mock import MagicMock
from unittest.mock import patch
from datetime import datetime

class Client:
    """
    Responsible for handling customer requests and communicating to the
    server for additional information.
    """

    def __init__(self, httpURL="http://127.0.0.1:8000"):
        """
        Attempts to connect to the http server.

        :param httpURL: The host URL to be communicated to.
        """
        tableToDir = {"table": "/table",
                      "booking": "/booking",
                      "order": "/order",
                      "menu": "/menu"}

        self.tableToURL = {}
        for table, dir in tableToDir.items():
            self.tableToURL[table] = httpURL + dir

    def fetchData(self, table, query=None):
        """
        Queries the server to return more data for the given query and table.

        :param table: Name of the table to be queried on the server. The name
        should be in the tableToURL dictionary.
        :param query: A dictionary of fields that will be used to help search
        the table.
        :return: All data available for the given query.
        """
        response = requests.get(self.tableToURL[table], params=query)
        return response.text

    def sendData(self, table, data):
        """
        Sends data to the server to store in the database.

        :param table: Name of the table where the data will be stored.
        :param data: A dictionary of fields to be stored in the database.
        """
        requests.post(self.tableToURL[table], params=data)


class ClientTest(unittest.TestCase):
    """
    Unit test class for Customer.
    """

    @patch("requests.get")      # Overrides the request.get method
    def testFetchData(self, requestGetMethod):
        """
        Tests whether the client can fetch data from a mock object
        representing the server.
        """
        tableData = {"reference": "FJ802035DT",
                     "date": "10-10-1000",
                     "name": "programmer K",
                     "phone": "01123581321",
                     "email": "programmerK@gmail.com",
                     "table number": "99",
                     "sanity": "-9000"}

        query = {"name": "programmer K"}

        mockResponse = MagicMock()
        mockResponse.text = tableData
        requestGetMethod.return_value = mockResponse

        client = Client()
        self.assertDictEqual(client.fetchData("booking", query), tableData)

        with self.assertRaises(KeyError):
            client.fetchData("death list", query)

    @patch("requests.post")      # Overrides the request.post method
    def testFetchData(self, requestPostMethod):
        """
        Tests whether the client can send data to a mock object representing
        the server.
        """
        tableData = {"reference": "FJ802035DT",
                     "date": "10-10-1000",
                     "name": "programmer K",
                     "phone": "01123581321",
                     "email": "programmerK@gmail.com",
                     "table number": "99",
                     "sanity": "-9000"}

        client = Client()
        client.sendData("order", tableData)
        url = "http://127.0.0.1:8000/order"
        requestPostMethod.assert_called_once_with(url, params=tableData)


class Reservation:
    """
    Responsible for issuing booking and cancellation requests to the server.
    """

    def __init__(self):
        """
        Initializes a menu and table objects which represent the restaurant's
        menu and tables.
        """
        self.reservationInfo = []

    def reserve(self, isBook, tableNum, timeFrame):
        """
        Applies a booking or cancellation of a table.

        :param isBook: Boolean of whether the book or cancel
        :param tableNum: The table number to be booked.
        :param timeFrame: Datetime object of the start time of the booking.
        :return: A dictionary that contains the booking information
        """
        d = timeFrame.date()
        t = timeFrame.time()

        bookingDict = {"table": tableNum,
                       "book": isBook,
                       "date": (d.year, d.month, d.day),
                       "time": (t.hour, t.minute)}
        return bookingDict


class ReservationTest(unittest.TestCase):
    """
    Unit test class for Reservation.
    """

    def setUp(self):
        """
        Creates a Reservation object.
        """
        self.reservation = Reservation()

    def testReserve(self):
        """
        Tests whether the information generated from a booking or cancellation
        request is correct.
        """
        bookingInfo = \
            self.reservation.reserve(True, 3, datetime(2005, 7, 14, 12, 30))

        self.assertEqual(bookingInfo["table"], 3)
        self.assertEqual(bookingInfo["date"], (2005, 7, 14))
        self.assertEqual(bookingInfo["time"], (12, 30))
        self.assertEqual(bookingInfo["book"], True)

        bookingInfo = \
            self.reservation.reserve(False, 3, datetime(2005, 7, 14, 12, 30))

        self.assertEqual(bookingInfo["book"], False)


class Restaurant:
    """
    Represents the restaurant which is responsible for dealing with customers
    currently in the restaurant. This includes managing table requests.
    """

    def __init__(self, menu, tableAmount):
        """
        Initializes a menu and table objects which represent the restaurant's
        menu and tables.
        """
        self.tables = []
        self.menu = menu

        for i in range(tableAmount):
            self.tables.append(Table(i, self.menu))

    def findEmptyTable(self):
        """
        Finds and returns a list of tables that are currently not being used by
        any customer.
        :return: A list of table objects that are available to be used.
        """
        availableTables = []
        for table in self.tables:
            if(table.isAvailable):
                availableTables.append(table)
        return availableTables


class RestaurantTest(unittest.TestCase):
    """
    Unit test class for Restaurant.
    """

    @patch("client.Table")
    def setUp(self, mockTable):
        """
        Creates a restaurant object with a mock menu prior to each test.
        :param mockTable: A mock object of a table.
        """
        menu = self.setUpMenu()
        mockTable.side_effect = self.createMockTable
        self.restaurant = Restaurant(menu, 50)

    def setUpMenu(self):
        """
        Sets up a dummy menu to be used for testing.
        :return: A mock menu object.
        """
        woodInfo = ["wood", 123.00]
        breadInfo = ["bread", 111.00]
        cardboardInfo = ["cardboard", 321.00]

        foodInfo = [woodInfo, breadInfo, cardboardInfo]
        foodList = []

        for info in foodInfo:
            food = MagicMock()
            food.name = info[0]
            food.price = info[1]
            foodList.append(food)

        menu = MagicMock()
        menu.items = foodList
        return menu

    def createMockTable(self, *args, **kwargs):
        """
        Creates and returns a mock table.
        :return: A prepared mock table.
        """
        mockTable = MagicMock()
        mockTable.isAvailable = False
        return mockTable

    def testFindEmptyTable(self):
        """
        Tests whether available table can be found.
        """
        tableList = []
        tableNum = [11, 22, 33]

        # Initialize Empty tables
        for i, num in enumerate(tableNum):
            tableList.append(self.restaurant.tables[num])
            tableList[i].isAvailable = True

        emptyTables = self.restaurant.findEmptyTable()

        for i, empty in enumerate(emptyTables):
            self.assertEqual(empty, tableList[i])


class Table:
    """
    Represents a restaurant table (essentially customer requests).
    """

    def __init__(self, tableNum, menu):
        """
        Initializes some fields while delaying others until need be.

        :param tableNum: The number of the table.
        :param menu: A menu object that represents the restaurant menu.
        """
        self.menu = menu
        self.num = tableNum
        self.isOccupied = False
        self.hasOrdered = False
        self.size = None
        self.orderHistory = []
        self.totalPaid = 0.0

    def order(self, foodName):
        """
        Registers an order into the history.

        To be precise, checks whether the provided food name is part of the
        menu, if so then pulls the food object from the menu and stores it
        in the order history field.

        :param foodName: The name of the food object to be ordered.
        """
        isInMenu = False

        for food in self.menu.items:
            if food.name == foodName.lower():
                self.orderHistory.append(food)
                isInMenu = True

        if not isInMenu:
            raise NameError("{} is not part of the menu".format(foodName))

    def computeBill(self):
        """
        Calculates the total price of all the food ordered.
        :return: The total bill for the table.
        """
        totalBill = 0
        for food in self.orderHistory:
            totalBill += food.price
        return totalBill

    def payBill(self, payment):
        """
        Simulates the payment for the total bill.

        For now, it is simply just storing the supplied argument into the
        totalPaid field but can be subject to change if need be.

        :param payment: The amount paid by the customer.
        """
        self.totalPaid += payment

    def printAllOrders(self):
        """
        Prints all the orders requested by the table which are stored in the
        orderHistory field.
        """
        separatorTemplate = "{:#<40}".format("")
        headerTemplate = "{0:#<16} ORDERS {0:#<16}".format("")

        print(headerTemplate)
        for food in self.orderHistory:
            print(food)
        print(separatorTemplate)

    def printBill(self):
        """
        Prints the total bill of all orders from the table.
        """
        print("Total Bill: {:.2f} GBP".format(self.computeBill()))


class TableTest(unittest.TestCase):
    """
    Unit test class for the Table class.
    """

    def setUp(self):
        """
        Initialises a table object prior to each test using mock objects.
        """
        menu = self.setUpMenu()
        self.table = Table(10, menu)

    def setUpMenu(self):
        """
        Sets up a dummy menu to be used for testing.
        :return: A mock menu object.
        """
        woodInfo = ["wood", 123.00]
        breadInfo = ["bread", 111.00]
        cardboardInfo = ["cardboard", 321.00]

        foodInfo = [woodInfo, breadInfo, cardboardInfo]
        foodList = []

        for info in foodInfo:
            food = MagicMock()
            food.name = info[0]
            food.price = info[1]
            foodList.append(food)

        menu = MagicMock()
        menu.items = foodList
        return menu

    def testOrder(self):
        """
        Tests whether the order method registers orders properly.
        """
        self.table.order("wood")
        self.table.order("wood")

        # Orders actually requested
        self.assertTrue(len(self.table.orderHistory), 2)
        self.assertTrue(self.table.orderHistory[0].name, "wood")

        # Orders not requested
        with self.assertRaises(NameError):
            self.table.order("metal")

    def testComputeBill(self):
        """
        Tests whether the bill matches the dollar.
        """
        self.table.order("wood")
        self.table.order("bread")
        self.table.order("cardboard")
        self.assertEqual(self.table.computeBill(), 555.00)

    def testPayBill(self):
        """
        Tests whether the payBill method properly accumulates payments.
        """
        self.table.payBill(10.00)
        self.table.payBill(10.00)
        self.table.payBill(20.00)
        self.table.payBill(30.00)
        self.table.payBill(50.00)
        self.assertEqual(self.table.totalPaid, 120.00)


class Menu:
    """
    Represents the restaurant menu.
    """

    def __init__(self, foodItems=None):
        """
        Constructs the menu and adds food objects into the items field.

        :param foodItems: A list (or tuple) of Food objects to be added
                          to the menu.
        """
        self.items = MenuSet()

        if foodItems:
            for food in foodItems:
                self.items.add(food)

    def findItem(self, foodName):
        """
        Attempts to find the given food name on the menu and then returns the
        food object. If the name cannot be found, then raises a NameError
        exception.

        :param foodName: The name of the food to be searched.
        :return: The Food object being looked up otherwise a NameError.
        """
        for food in self.items:
            if food.name == foodName.lower():
                return food

        raise NameError("{} is not on the menu.".format(foodName))

    def printMenu(self):
        """
        Prints the restaurant menu.
        """
        headerTemplate = "{0:#<17} MENU {0:#<17}".format("")
        separatorTemplate = "{:#<40}".format("")

        # Prints the header
        print(headerTemplate)
        print(separatorTemplate + "\n")

        # Prints the body
        for food in self.items:
            print(food)

        # Prints the footer
        print(separatorTemplate)


class MenuTest(unittest.TestCase):
    """
    Unit test class for Menu class.
    """

    def setUp(self):
        """
        Prepares a menu to be tested against using mock objects.
        """
        self.bread = MagicMock()
        self.cardboard = MagicMock()

        self.bread.name = "bread"
        self.cardboard.name = "cardboard"
        foodItems = [self.cardboard, self.bread]

        self.menu = Menu(foodItems)

    def testFindItem(self):
        """
        Tests whether a specified food item can be found on the menu.
        """
        # Items on the menu

        self.assertEqual(self.menu.findItem("bread"), self.bread)
        self.assertEqual(self.menu.findItem("cardboard"), self.cardboard)

        # Items not on the menu
        with self.assertRaises(NameError):
            self.menu.findItem("salvation")


class MenuSet(set):
    """
    A simple set class that has the same properties as a set class
    except that it warns the user if the entry being added already exists.
    """

    def add(self, element):
        """
        Adds an element into the set but warns the user if the element
        already exists in the set.

        :param element: The element to be added to the set.
        """
        if element in self:
            print("WARNING: Overriding an existing element.")

        # Uses the superclass 'add' method
        super(MenuSet, self).add(element)


class MenuSetTest(unittest.TestCase):
    """
    Unit test class for the MenuSet class.
    """

    def testAddingItem(self):
        """
        Tests whether the overridden add method behaves similar
        to the super class method (i.e. everything should be identical
        excluding a print statement upon adding a duplicate element).
        """
        itemA = "Item A"
        itemB = "Item B"

        menuSet = MenuSet()
        menuSet.add(itemA)
        menuSet.add(itemA)
        menuSet.add(itemB)

        self.assertEqual(len(menuSet), 2)
        self.assertTrue(itemA in menuSet)
        self.assertTrue(itemB in menuSet)


class Food:
    """
    Represents a meal item on a menu (can be a drink).
    """

    def __init__(self, foodInfo):
        """
        Constructs a food object.

        :param foodInfo: A list (or tuple) of the form
                         <name, description, price>.
        """
        self.name = foodInfo[0]
        self.type = foodInfo[1]
        self.description = foodInfo[2]
        self.price = foodInfo[3]

    def __str__(self):
        """
        String representation of the food object.
        """
        nameString =  "Item: {}\n".format(self.name.capitalize())
        typeString = "Type: {}\n".format(self.type.capitalize())
        descriptionString  = \
            "Description: {}\n".format( self.description.capitalize())
        priceString = "Price: {:.2f} GBP\n".format(self.price)

        template = nameString + typeString + descriptionString + priceString
        return template

    @property
    def name(self):
        """
        :return: The name of the food.
        """
        return self._name

    @name.setter
    def name(self, foodName):
        """
        :param foodName: The name of the food must be non-empty string.
        """
        if not foodName:
            raise ValueError("The food name cannot be empty.")
        self._name = foodName.lower()

    @property
    def type(self):
        """
        :return: The type of the dishes--
                 (starter, main course, dessert, beverage).
        """
        return self._type

    @type.setter
    def type(self, foodType):
        """
        :param foodName: The name of the food must be non-empty string.
        """
        validFoodTypes = ["starter", "main course", "dessert", "beverage"]

        if foodType.lower() not in validFoodTypes:
            errorMessage = ("The food type is invalid. "
                            "It can only be of type: ")
            for validFood in validFoodTypes:
                errorMessage += "{}, ".format(validFood)
            errorMessage.rstrip(",")

            raise ValueError(errorMessage)
        self._type = foodType.lower()

    @property
    def description(self):
        """
        :return: The description of the food.
        """
        return self._description

    @description.setter
    def description(self, foodDescription):
        """
        :param foodDescription: The name of the food must be non-empty string.
        """
        if not foodDescription:
            raise ValueError("The food description cannot be empty.")
        self._description = foodDescription.lower()

    @property
    def price(self):
        """
        :return: The price of the food.
        """
        return self._price

    @price.setter
    def price(self, foodPrice):
        """
        :param foodPrice: The name of the food must be a non-negative number.
        """
        try:
            int(foodPrice)
        except:
            raise TypeError("The food price must be a number.")

        if foodPrice < 0:
            raise ValueError("The food price must be non-negative.")
        self._price = foodPrice


class FoodTest(unittest.TestCase):
    """
    Unit tests class for the Food class.
    """

    def testConstructor(self):
        """
        Tests whether constructing a valid food passes (and invalid fails).
        """
        # Valid food description
        validFood = ["Potato", "Main Course", "Very mushy...", 42.0]

        # Invalid food descriptions
        blankName = ["",  "Main Course", "Very mushy...", 42.0]
        blankDescription = ["Potato",  "Main Course", "", 42.0]
        invalidDishType = ["Potato", "MainCourse", "", 42.0]

        stringPrice = ["Potato",  "Main Course", "Very mushy...", "Kiwi"]
        negativePrice = ["Potato",  "Main Course", "Very mushy...", -42.0]
        blankPrice = ["Potato",  "Main Course", "Very mushy...", ""]
        emptyPrice = ["Potato",  "Main Course", "Very mushy...",]


        # Valid object
        potato = Food(validFood)
        self.assertEqual(potato.name, "potato")
        self.assertEqual(potato.type, "main course")
        self.assertEqual(potato.description, "very mushy...")
        self.assertEqual(potato.price, 42.0)

        # Invalid objects
        with self.assertRaises(ValueError):
            Food(blankName)
            Food(blankDescription)
            Food(invalidDishType)
            Food(negativePrice)
            Food(blankPrice)
            Food(emptyPrice)
        with self.assertRaises(TypeError):
            Food(stringPrice)


def testPrintStatements():
    """
    Runs all the print statements across all unit tested classes.
    This is factored out to avoid spam.
    """
    # Initialization
    cardboardInfo = ["cardboard", "dessert", "Fibericious", 42]
    breadInfo = ["bread", "main course", "I am BREAD.", 666]
    cardboard = Food(cardboardInfo)
    bread = Food(breadInfo)
    foodItems = [cardboard, bread]

    menu = Menu(foodItems)
    table = Table(7, menu)
    table.order("bread")
    table.order("bread")
    table.order("bread")

    # All print statements
#    menu.print()
#    table.printAllOrders()
#    table.printBill()


def main():
    """
    Code is executed through this method.
    """
    testPrintStatements()


if __name__ == "__main__":
#    main()
    unittest.main()