"""
A set of unit tests for the model module in the client package.
"""

__docformat__ = 'reStructuredText'

import json
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest.mock import call
from datetime import datetime

from aardvark.client.model import (
    Client, Table, Food, Menu, MenuSet, Reservation, Restaurant
)


class ClientTest(unittest.TestCase):
    """
    Unit test class for Customer.
    """

    def setUp(self):
        """
        Prepares some mock data for the Json menu and food, a mock menu,
        and a mock food object. Also, creates a Client object.
        """
        self.foodInfo = ["seaweed",
                         "breakfast",
                         "My hopes and dreams...",
                         11]

        self.jsonFood = \
        {
            "name": self.foodInfo[0],
            "type": self.foodInfo[1],
            "description": self.foodInfo[2],
            "price": self.foodInfo[3],
        }

        # The json style is identical to the way Django sends serialized
        # model data in json formatting. All keys are omitted except the
        # relevant key which is "fields"
        self.receivedJsonMenu = [{"fields": self.jsonFood},
                                 {"fields": self.jsonFood}]

        self.client = Client()
        self.setUpFood()
        self.setUpMenu()

    def setUpFood(self):
        """
        Sets up a dummy food object.
        """
        self.mockFood = MagicMock()
        self.mockFood.name = self.jsonFood["name"]
        self.mockFood.type = self.jsonFood["type"]
        self.mockFood.description = self.jsonFood["description"]
        self.mockFood.price = self.jsonFood["price"]

    def setUpMenu(self):
        """
        Sets up a dummy menu.
        """
        self.wood = MagicMock()
        self.wood.name = "wood"
        self.wood.type = "breakfast"
        self.wood.description = "delicious"
        self.wood.price = 123.00

        self.bread = MagicMock()
        self.bread.name = "bread"
        self.bread.type = "lunch"
        self.bread.description = "beefy..."
        self.bread.price = 111.00

        self.cardboard = MagicMock()
        self.cardboard.name = "cardboard"
        self.cardboard.type = "dinner"
        self.cardboard.description = "fiberlicious"
        self.cardboard.price = 321.00

        self.mockMenu = MagicMock()
        self.mockMenu.items = [self.wood, self.bread, self.cardboard]

    @patch("requests.post")
    def testSubmitOrder(self, mockRequestMethod):
        """
        Tests whether the client is able to submit ordered food items
        in the correct format.
        """
        orderedItems = {"banana": 3,
                        "orange": 10}
        tableNum = 3

        content = {"order": [{"name": "banana",
                              "quantity": 3,
                              "table": tableNum},

                             {"name": "orange",
                              "quantity": 10,
                              "table": tableNum}]}

        response = MagicMock()
        response.status_code = 200
        response.content = json.dumps(content)
        mockRequestMethod.return_value = response

        response = self.client.submitOrder(orderedItems, tableNum)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, json.dumps(content))


    @patch("requests.post")
    def testSendBookingDetails(self, mockRequestMethod):
        """
        Tests whether the client is able to send booking details in the
        correct format.
        """
        bookingDetails = {"name": "sherlock",
                          "email": "programmerK@gmail.com",
                          "phone": "07472440699",
                          "date":  "2016-04-03",
                          "time":  "23:15",
                          "table": "3",
                          "size": "5"}

        response = MagicMock()
        response.status_code = 200
        response.content = json.dumps(bookingDetails)
        mockRequestMethod.return_value = response

        response = self.client.sendBookingDetails(**bookingDetails)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, json.dumps(bookingDetails))

    @patch("requests.get")
    def testRequestTotalTables(self, mockRequestMethod):
        """
        Tests whether the client can fetch the total number of tables from a
        mock object representing the server.
        """
        response = MagicMock()
        response.text = totalTables = 50
        mockRequestMethod.return_value = response

        self.assertEqual(self.client.requestTotalTables().text, totalTables)

    @patch("requests.get")
    def testRequestAvailableSizes(self, mockRequestMethod):
        """
        Tests whether the client can fetch all the available table sizes for
        booking from a mock object representing the server.
        """
        data = {"sizes": ["2", "3", "5"]}

        response = MagicMock()
        response.status_code = 200
        response.content.decode.return_value = json.dumps(data)
        mockRequestMethod.return_value = response

        date, time = "2016-03-02", "09:00"
        availableTimes = self.client.requestAvailableSizes(date, time)
        self.assertEqual(availableTimes, data["sizes"])

    @patch("requests.get")
    def testRequestAvailableSizes(self, mockRequestMethod):
        """
        Tests whether the client can fetch all the available tables for
        booking from a mock object representing the server.
        """
        data = {"tables": ["2", "3", "5"]}

        response = MagicMock()
        response.status_code = 200
        response.content.decode.return_value = json.dumps(data)
        mockRequestMethod.return_value = response

        date, time, size = "2016-03-02", "09:00", "3"
        availableTimes = self.client.requestAvailableTables(date, time, size)
        self.assertEqual(availableTimes, data["tables"])

    @patch("aardvark.client.model.Client._parseJsonMenu")
    @patch("aardvark.client.model.Menu")
    @patch("requests.get")
    @patch("json.loads")
    def testRequestMenu(self, _, mockRequestMethod, mockMenu, mockParse):
        """
        Tests whether the client can fetch the menu from a mock object
        representing the server.
        """
        response = MagicMock()
        response.text = self.receivedJsonMenu
        response.status_code = 200

        mockRequestMethod.return_value = response
        mockParse.return_value = [self.mockFood, self.mockFood]

        menuArgs = call([self.mockFood, self.mockFood])
        self.client.requestMenu()
        self.assertEqual(mockMenu.call_args, menuArgs)

        response.status_code = 404
        self.client.requestMenu()
        self.assertEqual(mockMenu.call_args, "")

    @patch("aardvark.client.model.Food")
    @patch("aardvark.client.model.Client._parseJsonFood")
    def testParseJsonMenu(self, mockParse, mockFoodClass):
        """
        Tests whether data about menu in Json formatting can be parsed
        correctly (so that it can later be fed into the Menu constructor).
        """
        mockParse.return_value = self.foodInfo
        mockFoodClass.return_value = self.mockFood
        foodList = self.client._parseJsonMenu(self.receivedJsonMenu)

        self.assertListEqual(foodList, [self.mockFood, self.mockFood])

    def testParseJsonFood(self):
        """
        Tests whether data about menu in Json formatting can be parsed
        correctly (so that it can later be fed into the Food constructor).
        """
        foodData = self.client._parseJsonFood(self.jsonFood)
        self.assertEqual(foodData, self.foodInfo)

    def testConvertFoodToJson(self):
        """
        Tests whether a food object (mocked) can be parsed to Json
        formatting correctly.
        """
        self.assertDictEqual(self.client._convertFoodToJson(self.mockFood),
                             self.jsonFood)

    @patch("requests.post")
    def testSendMenu(self, requestPostMethod):
        """
        Tests whether the client can send the menu to a mock object
        representing the server.
        """
        mockResponse = MagicMock()
        mockResponse.text = self.receivedJsonMenu
        requestPostMethod.return_value = mockResponse

        response = self.client.sendMenu(self.mockMenu)

        self.assertTrue(len(response.text) == 2)
        for foodData in response.text:
            self.assertDictEqual(foodData["fields"], self.jsonFood)


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


class RestaurantTest(unittest.TestCase):
    """
    Unit test class for Restaurant.
    """

    @patch("aardvark.client.model.Table")
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
        Creates and returns a new modified mock table object per call.
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


class MenuTest(unittest.TestCase):
    """
    Unit test class for Menu class.
    """

    def setUp(self):
        """
        Constructs a TabMenu object
        """
        self.setUpFood()
        self.menu = Menu([self.wood, self.bread, self.cardboard])

    def setUpFood(self):
        """
        Sets up some mock food objects.
        """
        self.wood = MagicMock()
        self.wood.name = "wood"
        self.wood.type = "breakfast"
        self.wood.description = "delicious"
        self.wood.price = 123.00

        self.bread = MagicMock()
        self.bread.name = "bread"
        self.bread.type = "breakfast"
        self.bread.description = "delicious"
        self.bread.price = 321.00

        self.cardboard = MagicMock()
        self.cardboard.name = "cardboard"
        self.cardboard.type = "lunch"
        self.cardboard.description = "delicious"
        self.cardboard.price = 111.00

    def testCategorizeFood(self):
        """
        Tests whether the food items on the menu can be sorted based on
        their types.
        """
        foodType = {"breakfast": [self.wood, self.bread],
                    "lunch": [self.cardboard]}

        sortedType = self.menu.categorizeFood()

        self.assertTrue(self.wood in sortedType["breakfast"])
        self.assertTrue(self.bread in sortedType["breakfast"])
        self.assertFalse(self.cardboard in sortedType["breakfast"])

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


class MenuSetTest(unittest.TestCase):
    """
    Unit test class for the MenuSet class.
    """

    @patch("sys.stdout", None)
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


# def testPrintStatements():
#     """
#     Runs all the print statements across all unit tested classes.
#     This is factored out to avoid spam.
#     """
#     # Initialization
#     cardboardInfo = ["cardboard", "dessert", "Fibericious", 42]
#     breadInfo = ["bread", "main course", "I am BREAD.", 666]
#     cardboard = Food(cardboardInfo)
#     bread = Food(breadInfo)
#     foodItems = [cardboard, bread]
#
#     menu = Menu(foodItems)
#     table = Table(7, menu)
#     table.order("bread")
#     table.order("bread")
#     table.order("bread")
#
#     # All print statements
#     menu.print()
#     table.printAllOrders()
#     table.printBill()
#
#
# def main():
#    """
#    Code is executed through this method.
#    """
#    testPrintStatements()
