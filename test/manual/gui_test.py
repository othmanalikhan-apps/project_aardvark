"""
A simple functional test for the client GUI with mock data.

Things to ***manually*** test for:

##### 1.  Splash Screen:
Check Rendering:
* It should include: image, title, subtitle, continue button and a status bar.


##### 2. Menu Tab Screen:
Check Alignment:
* Food names should be on the left.
* The description should be in the middle but left aligned.
* The prices should be on the right.


##### 3. Order Tab Screen:
Check Navigation:
* First table screen should be able to enter the order screen by pressing any
button.
* The back button on the order screen should return back to the table screen.

Check Buttons:
* Clicking on any food button on the order screen adds selected item to the
ordered items list.
* Clicking the "+" and "-" buttons for ordered items adds and decreases/removes
the item.


##### 4. Booking Tab Screen:
Check Image:
* Ensure that the image appears to look fine and is not overstretched.

Check Booking Details Fields:
* Ensure that the time field has drop down options of time.
* Ensure that the table field has drop down options as integers.
* Ensure that the date field allows selection of a date on a calendar.

Check Customer Details Fields:
* Ensure that the name, email and phone number fields can be inputted


##### 5. Payment Tab Screen:
Check Navigation:
* First table screen should be able to enter the order screen by pressing any
button.
* The back button on the order screen should return back to the table screen.

Check Calculations Fields:
* Ensure that the "£" symbol is displayed left of all the fields to enter


##### 6. Help Tab Screen:
Check Alignment:
* Ensure that all the text looks decently aligned
* Ensure that the order of the sections is: "Quick Guide", "About Us",
"Contact Us", "Legal"
"""

__docformat__ = 'reStructuredText'

import os
import unittest
import csv

from aardvark.client.controller import MainController
from aardvark.client.model import Menu
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

    @patch("aardvark.client.model.Client.requestMenu")
    def testGUI(self, mockRequest):
        """
        Tests whether the GUI can be ran.
        """
        mockRequest.return_value = self.menu
        MainController()


if __name__ == "__main__":
    unittest.main()
