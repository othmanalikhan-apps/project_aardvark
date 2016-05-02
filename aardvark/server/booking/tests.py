import datetime
import json

from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.core.exceptions import ValidationError

from .models import Booking
from .views import updateBooking, sendBookingSlots
from table.models import Table

from unittest.mock import patch, MagicMock, call
from model_mommy import mommy
from copy import deepcopy


################################ UNITTESTS TESTS ###############################


class BookingModelTests(TestCase):
    """
    Unit tests for the Booking model class.
    """

    def setUp(self):
        """
        Creates an instance of the booking model and mock dependencies.
        """
        self.mockTable = mommy.make("table.Table")
        self.validBooking = Booking(name="sherlock",
                                    phone="07472440699",
                                    email="programmerK@gmail.com",
                                    date="2030-05-01",
                                    time="9:00",
                                    table=self.mockTable)

    def testConstructor(self):
        """
        Tests whether the object is constructed properly.
        """
        self.assertEqual(self.validBooking.name, "sherlock")
        self.assertEqual(self.validBooking.phone, "07472440699")
        self.assertEqual(self.validBooking.email, "programmerK@gmail.com")
        self.assertEqual(self.validBooking.date, "2030-05-01")
        self.assertEqual(self.validBooking.time, "9:00")
        self.assertEqual(self.validBooking.table, self.mockTable)

    def testValidation(self):
        """
        Tests whether model validation is working as intended.

        The tests below are brief and rather sloppy since most of the
        validation happens at the client end (i.e. sanitized input).
        """
        invalidLongName = deepcopy(self.validBooking)
        invalidLongName.name = "thisnameisratherelaboratelylongdon'tyousee?" \
                               "thisnameisratherelaboratelylongdon'tyousee?"

        invalidLongEmail = deepcopy(self.validBooking)
        invalidLongEmail.email = "thisnameisratherelaboratelylongdon'tyousee?"\
                                 "thisnameisratherelaboratelylongdon'tyousee?"

        invalidLongPhone = deepcopy(self.validBooking)
        invalidLongPhone.phone = "111111111111111111111111"

        invalidDate = deepcopy(self.validBooking)
        invalidDate.date = "Hello"

        invalidTimeChoice = deepcopy(self.validBooking)
        invalidTimeChoice.time = "5:00"

        try:
            self.validBooking.clean_fields()
        except Exception as e:
            self.fail("Instantiating the supposed valid object raised "
                      "the following error:\n{}".format(e))

        with self.assertRaises(ValidationError):
            invalidLongName.clean_fields()
            invalidLongEmail.clean_fields()
            invalidLongPhone.clean_fields()
            invalidDate.clean_fields()
            invalidTimeChoice.clean_fields()

    def testUniqueReferenceNumber(self):
        """
        Tests whether model instances have unique reference numbers
        """
        booking = Booking(name="sherlock",
                          phone="07472440699",
                          email="programmerK@gmail.com",
                          date="2030-05-01",
                          time="22:15",
                          table=self.mockTable)

        self.assertNotEqual(self.validBooking.reference, booking.reference)

    def test__str__(self):
        """
        Tests whether the __str__ magic method was override properly.
        """
        self.assertEqual(str(self.validBooking), self.validBooking.name)


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

        self.slotsAvailable = {"1": ["14:00", "15:00", "16:00"],
                               "2": [],
                               "3": ["14:00", "16:00"]}

    @patch("booking.views.Booking")
    @patch("booking.views.Table")
    def testUpdateBooking(self, mockTable, mockBooking):
        """
        Tests whether the server is able to receive booking information from
        the client and handle it correctly.
        """
        mockRequest = MagicMock()
        mockRequest.method = "POST"

        mockTable.objects.get.return_value = mommy.make("table.Table")
        mockBooking.objects.create.return_value = MagicMock(reference="112")

        with patch("booking.views.json.loads") as mockJsonLoad:
            mockJsonLoad.return_value = self.bookingData
            response = updateBooking(mockRequest)

        data = json.loads(response.content.decode("utf-8"))
        refNum = data["reference"]

        createArgs = [call(**self.bookingData)]

        self.assertEqual(mockBooking.objects.create.call_args_list, createArgs)
        self.assertEqual(refNum, "112")


############################### INTEGRATION TESTS ##############################


class IntegrationTests(TestCase):
    """
    Integration tests for the booking app.
    """

    def setUp(self):
        """
        Declares booking data.
        """
        self.bookingData = {"name": "sherlock",
                            "phone": "07472440699",
                            "email": "programmerK@gmail.com",
                            "date":  "2016-04-03",
                            "time":  "11:00",
                            "table": "3"}

    def testReceiveBookingFromClient(self):
        """
        Tests whether the server is able to receive booking information from
        the client and successfully store it into the database.
        """
        Table.objects.create(number=3)

        client = Client()
        response = client.post(reverse("booking-update"),
                               json.dumps(self.bookingData),
                               content_type="application/json")

        validBooking = Booking.objects.get(name="sherlock")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(validBooking.time, datetime.time(11, 00))

    def testSendBookingSlotsToClient(self):
        """
        Tests whether the server is able to calculate booking slots for a
        given date and send the data to the client.
        """
        table1 = Table.objects.create(number=1)
        table2 = Table.objects.create(number=2)
        table3 = Table.objects.create(number=3)

        booking1 = Booking.objects.create(name="sherlock",
                                          phone="07472440699",
                                          email="programmerK@gmail.com",
                                          date="2030-05-01",
                                          time="9:00",
                                          table=table1)

        booking2 = Booking.objects.create(name="sherlock",
                                          phone="07472440699",
                                          email="programmerK@gmail.com",
                                          date="2030-05-01",
                                          time="13:00",
                                          table=table2)

        availableSlots = {"1": ["11:00", "13:00", "15:00"],
                          "2": ["09:00", "11:00", "15:00"],
                          "3": ["09:00", "11:00", "13:00", "15:00"]}

        client = Client()
        response = client.get(reverse("booking-send", args=["2030-05-01"]))
        slots = json.loads(response.content.decode("utf-8"))

        for tableNum in availableSlots:
            self.assertListEqual(slots[tableNum], availableSlots[tableNum])
