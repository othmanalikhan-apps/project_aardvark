"""
A simple functional test for the client GUI with mock data.
"""

__docformat__ = 'reStructuredText'

import os
import unittest
import csv

from src.client.controller import MainController
from src.client.model import Menu
from unittest.mock import MagicMock, patch


class GUITest(unittest.TestCase):
    """
    Functional test of the GUI with a mock data.

    Just ensures that the GUI is able to run. The rest of the testing is done
    manually by browsing around the GUI as oppose to using some framework (
    would require a time warp).
    """

    def setUp(self):
        """
        Sets up a menu using mock data from a prepared csv file.
        """
        items = []
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "mock_menu.csv")

        with open(path) as csvFile:
            reader = csv.reader(csvFile, delimiter=";")
            for foodRow in reader:
                if foodRow:
                    mockFood = MagicMock()
                    mockFood.name = foodRow[0].strip()
                    mockFood.type = foodRow[1].strip()
                    mockFood.description = foodRow[2].strip()
                    mockFood.price = float(foodRow[3].strip())
                    items.append(mockFood)

        self.menu = Menu(items)

    @patch("src.client.model.Client.requestMenu")
    def testGUI(self, mockRequest):
        """
        Tests whether the GUI can be ran.
        """
        mockRequest.return_value = self.menu
        MainController()


if __name__ == "__main__":
    unittest.main()
