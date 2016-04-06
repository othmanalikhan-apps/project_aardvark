"""
The client side of the restaurant server-client system
"""

__docformat__ = 'reStructuredText'

import unittest
import requests


class Menu:
    """
    Represents the restaurant menu.
    """

    def __init__(self, foodItems=None):
        """
        :param foodItems: A list (or tuple) of Food objects to be added
                          to the menu.
        """
        self.items = MenuSet()

        if foodItems:
            for food in foodItems:
                self.items.add(food)

    def findItem(self, foodName):
        """
        :param foodName: The name of the food to be searched.
        :return: The Food object being looked up otherwise a NameError.
        """
        for item in self.items:
            if item.name == foodName.lower():
                return item

        raise NameError("{} is not on the menu.".format(foodName))

    def print(self):
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
        Prepares a menu to be tested against.
        """
        cardboardInfo = ["cardboard", "dessert", "Fibericious", 42]
        breadInfo = ["bread", "main course", "I am BREAD.", 666]

        self.cardboard = Food(cardboardInfo)
        self.bread = Food(breadInfo)
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
        """
        if element in self:
            print("Warning: Overriding an existing element.")

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

    # All print statements
#    menu.print()


def main():
    """
    Code is executed through this method.
    """
    testPrintStatements()


if __name__ == "__main__":
#    main()
    unittest.main()
