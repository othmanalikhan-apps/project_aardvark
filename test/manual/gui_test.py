"""
A simple functional test for the client GUI with mock data.
"""


__docformat__ = 'reStructuredText'


import unittest
import csv

from src.client.controller import main
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
        Constructs a TabMenu object
        """
        self.setUpMenu()

    def setUpMenu(self):
        """
        Sets up a dummy menu using mock data from a prepared csv file.
        """
        self.menu = MagicMock()
        self.menu.items = []

        with open("mock_menu.csv") as csvFile:
            reader = csv.reader(csvFile, delimiter=";")
            for foodRow in reader:
                if foodRow:
                    mockFood = MagicMock()
                    mockFood.name = foodRow[0].strip()
                    mockFood.type = foodRow[1].strip()
                    mockFood.description = foodRow[2].strip()
                    mockFood.price = float(foodRow[3].strip())
                    self.menu.items.append(mockFood)

    @patch("src.client.model.Client.requestMenu")
    def testGUI(self, mockRequest):
        """
        Tests whether the GUI can be ran.
        """
        mockRequest.return_value = self.menu
        main()


if __name__ == "__main__":
    unittest.main()
