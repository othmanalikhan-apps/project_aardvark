"""
A set of unit tests for the view module in the src.client package.
"""


__docformat__ = 'reStructuredText'


import unittest

from io import StringIO
from unittest.mock import MagicMock, patch

from src.client.view import (
    getStyle, TabMenu, getSocket
)


class ViewTest(unittest.TestCase):
    """
    Unittests for the standalone functions in the view module.
    """

    def testGetStyle(self):
        """
        A limited amount of testing since this method is influenced by the
        operating system; checks whether a style is found.
        """
        self.assertNotEqual(getStyle(), [])

    @patch("os.path.exists")
    @patch("builtins.open")
    def testGetSocket(self, mockOpen, mockPathExists):
        """
        Tests whether a server socket is readable from a mock
        configuration file.
        """
        properSettings = "[Network]\n" \
                         "serversocket=127.0.0.1:8000"
        blankSettings = "[Network]\n" \
                        "serversocket= "

        mockPathExists.return_value = True

        mockOpen.return_value = StringIO(properSettings)
        self.assertEqual(getSocket(), "127.0.0.1:8000")

        mockOpen.return_value = StringIO(blankSettings)
        self.assertEqual(getSocket(), "")


class TabMenuTest(unittest.TestCase):
    """
    Unittests for the helper functions in the TabMenu class.
    """

    def setUp(self):
        """
        Constructs a TabMenu object
        """
        self.setUpFood()
        self.setUpMenu()

    def setUpMenu(self):
        """
        Sets up a dummy menu.
        """
        self.menu = MagicMock()
        self.menu.items = [self.wood, self.bread, self.cardboard]

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

        self.assertDictEqual(TabMenu.categorizeFood(self.menu), foodType)


if __name__ == "__main__":
    unittest.main()
