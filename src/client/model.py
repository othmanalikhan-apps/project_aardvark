"""
The client side of the restaurant server-client system
"""

__docformat__ = 'reStructuredText'

import requests


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

    def requestMenu(self):
        """
        Requests the menu from the server.
        :return: An instantiated Menu object.
        """
        response = requests.get(self.tableToURL["menu"])
        parsedData = self.parseJsonMenu(response.text)
        return Menu(parsedData)

    def parseJsonMenu(self, JsonMenu):
        """
        Parses Json input containing data about the menu to a suitable form
        that can be directly passed into the Menu constructor.

        :param JsonMenu: The Json text containing data about the menu.
        :return: A list of Food objects (can be used to construct a Menu
        object).
        """
        foodList = []

        for foodData in JsonMenu["menu"]:
            parsedData = self.parseJsonFood(foodData)
            foodList.append(Food(parsedData))

        return foodList

    def parseJsonFood(self, JsonInput):
        """
        Parses Json input containing data about the food to a suitable form
        that can be directly passed into the Food constructor.

        :param JsonInput: The Json text containing data about the food.
        :return: A list containing food data (can be used to construct a Food
        object).
        """
        foodData = []
        dataAttributes = ["name", "type", "description", "price"]

        for attribute in dataAttributes:
            foodData.append(JsonInput[attribute])
        return foodData

    def convertFoodToJson(self, food):
        """
        Converts a supplied food object into Json format.

        :param food: A food object.
        :return: The food object parsed into Json formatting (dictionary).
        """
        JsonFormat = {}
        JsonFormat["name"] = food.name
        JsonFormat["type"] = food.type
        JsonFormat["description"] = food.description
        JsonFormat["price"] = food.price
        return JsonFormat

    def sendMenu(self, menu):
        """
        Sends the server the menu in Json form.
        :return: Response code of the post request.
        """
        JsonMenu = {"food": []}

        for food in menu.items:
            JsonFood = self.convertFoodToJson(food)
            JsonMenu["food"].append(JsonFood)

        response = requests.post(self.tableToURL["menu"], data=JsonMenu)
        return response


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


if __name__ == "__main__":
    pass

