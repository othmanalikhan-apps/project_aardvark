import requests
from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.core.exceptions import ValidationError

from .views import updateOrder
from .models import Order
from table.models import Table
from menu.models import Food

from unittest.mock import patch, MagicMock, call
from model_mommy import mommy

import json

################################ UNITTESTS TESTS ###############################


class OrderModelTests(TestCase):
    """
    Unit tests for the Booking model class.
    """

    def setUp(self):
        """
        Creates an instance of the order model and mock dependencies.
        """
        self.mockTable = mommy.make("table.Table")
        self.mockFood = mommy.make("menu.Food")
        self.validOrder = Order(table=self.mockTable,
                                food=self.mockFood)

    def testConstructor(self):
        """
        Tests whether the object is constructed properly.
        """
        self.assertEqual(self.validOrder.table, self.mockTable)
        self.assertEqual(self.validOrder.food, self.mockFood)

class ViewTests(TestCase):
    """
    Unit tests for the methods in the views file.
    """

    def setUp(self):
        """
        Declares order data, a mock table and food model.
        """
        self.orderData = {"order": [{"table": 1,
                                     "food": "banana",
                                     "quantity": 10},

                                    {"table": 2,
                                     "food": "orange",
                                     "quantity": 1111}]}

        self.mockTable = mommy.make("table.Table")
        self.mockFood = mommy.make("menu.Food")

    @patch("order.views.Order")
    @patch("order.views.Table")
    @patch("order.views.Food")
    def testUpdateOrder(self, mockFood, mockTable, mockOrder):
        """
        Tests whether the server is able to receive orders from the client
        and handle it correctly.
        """
        mockRequest = MagicMock()
        mockRequest.method = "POST"
        mockRequest.body.decode.return_value = json.dumps(self.orderData)

        mockFood.objects.get.return_value = self.mockFood
        mockTable.objects.get.return_value = self.mockTable
        mockOrder.objects.create.return_value = MagicMock()

        response = updateOrder(mockRequest)

        calls = [call(table=self.mockTable, food=self.mockFood, quantity=10),
                 call(table=self.mockTable, food=self.mockFood, quantity=1111)]

        self.assertEqual(response.status_code, requests.codes.ok)
        mockOrder.objects.create.assert_has_calls(calls)


############################### INTEGRATION TESTS ##############################


class IntegrationTests(TestCase):
    """
    Integration tests for the order app.
    """

    def setUp(self):
        """
        Declares order data and creates some entries in a mock database.
        """
        self.orderData = {"order": [{"table": 1,
                                     "food": "banana",
                                     "quantity": 10},

                                    {"table": 2,
                                     "food": "orange",
                                     "quantity": 1111}]}

        self.table1 = Table.objects.create(number=1, size=2)
        self.table2 = Table.objects.create(number=2, size=3)

        food1 = Food.objects.create(name="banana",
                                    type="main course",
                                    description="delicious",
                                    price=10.00,
                                    popularity=3)

        food2 = Food.objects.create(name="orange",
                                    type="breakfast",
                                    description="crunchy",
                                    price=12.00,
                                    popularity=13)

    def testReceiveOrderFromClient(self):
        """
        Tests whether the server is able to receive order information from
        the client and successfully store it into the database.
        """
        client = Client()
        response = client.post(reverse("order-update"),
                               json.dumps(self.orderData),
                               content_type="application/json")

        order = Order.objects.get(table=self.table1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(order.table.number, 1)
        self.assertEqual(order.food.price, 10.00)

