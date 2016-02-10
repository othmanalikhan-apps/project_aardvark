"""
The client side of the restaurant server-client system
"""

__docformat__ = 'reStructuredText'

import unittest
import requests


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


if __name__ == "__main__":
    unittest.main()
