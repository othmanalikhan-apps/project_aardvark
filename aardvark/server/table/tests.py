import datetime
import json

from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.core.exceptions import ValidationError

from .models import Table
from .views import sendTotalTables

from unittest.mock import patch, MagicMock, call
from model_mommy import mommy
from copy import deepcopy


################################ UNITTESTS TESTS ###############################


class TableModelTests(TestCase):
    """
    Unit tests for the Booking model class.
    """

    def setUp(self):
        """
        Creates an instance of the table model and mock dependencies.
        """
        self.mockOrder = mommy.make("order.Order")
        self.validTable = Table(number="3",
                                size="5",
                                order=self.mockOrder)

    def testConstructor(self):
        """
        Tests whether the object is constructed properly.
        """
        self.assertEqual(self.validTable.number, "3")
        self.assertEqual(self.validTable.size, "5")
        self.assertEqual(self.validTable.order, self.mockOrder)

    def testValidation(self):
        """
        Tests whether model validation is working as intended.

        The tests below are brief and rather sloppy since most of the
        validation happens at the client end (i.e. sanitized input).
        """
        invalidStringName = deepcopy(self.validTable)
        invalidStringName.number = "three"

        invalidStringSize = deepcopy(self.validTable)
        invalidStringSize.size = "five"

        try:
            self.validTable.clean_fields()
        except Exception as e:
            self.fail("Instantiating the supposed valid object raised "
                      "the following error:\n{}".format(e))

        with self.assertRaises(ValidationError):
            invalidStringName.clean_fields()
            invalidStringSize.clean_fields()

    def test__str__(self):
        """
        Tests whether the __str__ magic method was override properly.
        """
        self.assertEqual(str(self.validTable), self.validTable.number)

class ViewTests(TestCase):
    """
    Unit tests for the methods in the views file.
    """

    def setUp(self):
        """
        Declares some booking and slots data.
        """
        self.bookingData = {"name": "sherlock",
                            "phone": "07472440699",
                            "email": "programmerK@gmail.com",
                            "date":  "2016-04-03",
                            "time":  "23:15",
                            "table": "3"}

    @patch("table.views.Table")
    def testSendTableSize(self, mockTable):
        """
        Tests whether the server is able to find all tables and then
        send the information to the client.
        """
        table1 = MagicMock(number=1)
        table2 = MagicMock(number=3)
        table3 = MagicMock(number=3333)
        tables = [table1, table2, table3]
        tableNumbers = [table1.number, table2.number, table3.number]

        mockRequest = MagicMock()
        mockRequest.method = "GET"
        mockTable.objects.all.return_value = tables

        response = sendTotalTables(mockRequest)
        data = json.loads(response.content.decode("utf-8"))
        self.assertEqual(data["tables"], tableNumbers)
