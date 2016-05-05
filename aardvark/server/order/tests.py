import requests
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from .views import updateOrder, calculateBill, updateBill
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

                                    {"table": 1,
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

        calls = [call(table=self.mockTable,
                      food=self.mockFood,
                      quantity=10,
                      isHistory=False),
                 call(table=self.mockTable,
                      food=self.mockFood,
                      quantity=1111,
                      isHistory=False)]

        self.assertEqual(response.status_code, requests.codes.ok)
        mockOrder.objects.create.assert_has_calls(calls)

    @patch("order.views.Order")
    @patch("order.views.Table")
    def testCalculateBill(self, mockTable, mockOrder):
        """
        Tests whether the server is able to calculate the bill for a table from
        the client.
        """
        requestData = {"table": 1}
        mockRequest = MagicMock()
        mockRequest.method = "GET"
        mockRequest.body.decode.return_value = json.dumps(requestData)

        order = MagicMock()
        order.food.price = 10
        order.quantity = 3

        mockTable.objects.get.return_value = MagicMock()
        mockOrder.objects.filter.return_value = [order]

        response = calculateBill(mockRequest)
        data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, requests.codes.ok)
        self.assertEqual(data["bill"], 30)

    @patch("order.views.Order")
    @patch("order.views.Table")
    def testCalculateBill(self, mockTable, mockOrder):
        """
        Tests whether the server is able to calculate the bill for a table from
        the client.
        """
        requestData = {"paid": 100, "table": 3}
        mockRequest = MagicMock()
        mockRequest.method = "POST"
        mockRequest.content.decode.return_value = json.dumps(requestData)

        order = MagicMock()
        order.isPaid = False

        mockTable.objects.get.return_value = MagicMock()
        mockOrder.objects.filter.return_value = [order]

        response = updateBill(mockRequest)

        self.assertEqual(response.status_code, requests.codes.ok)
        self.assertEqual(order.isPaid, True)


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

        order1 = Order.objects.create(table=self.table1,
                                      food=food1,
                                      quantity=100,
                                      isHistory=False)

        order2 = Order.objects.create(table=self.table1,
                                      food=food1,
                                      quantity=100,
                                      isHistory=True)


    def testReceiveOrderFromClient(self):
        """
        Tests whether the server is able to receive order information from
        the client and successfully store it into the database.
        """
        client = Client()
        response = client.post(reverse("order-update"),
                               json.dumps(self.orderData),
                               content_type="application/json")

        order = Order.objects.filter(table=self.table1, isHistory=False)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(order[0].table.number, 1)
        self.assertEqual(order[0].food.price, 10.00)

    def testCalculateBillForClient(self):
        """
        Tests whether the server is able to calculate the bill for a given
        table supplied from the client and return the results.
        """
        data = {"table": 1}
        client = Client()
        response = client.get(reverse("order-bill"), data)
        billData = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(billData["bill"], 1000)

    def testUpdateBillForClient(self):
        """
        Tests whether the server is able to update the bill for a given
        table supplied from the client.
        """
        data = {"table": 1, "paid": 120.50}
        client = Client()
        response = client.post(reverse("order-payment"), data)

        self.assertEqual(response.status_code, 200)
