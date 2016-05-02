from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from django.core.exceptions import ValidationError

from .models import Food
from .views import updateMenu, sendMenu

from unittest.mock import patch, MagicMock, call
from copy import deepcopy

import json


################################ UNITTESTS TESTS ###############################


class FoodModelTests(TestCase):
    """
    Unit tests for the Food model class.
    """

    def setUp(self):
        """
        Creates an instance of the food model.
        """
        self.validFood = Food(name="burger",
                              type="main course",
                              description="delicious",
                              price=10.00,
                              popularity=3)

    def testConstructor(self):
        """
        Tests whether the object is constructed properly.
        """
        self.assertEqual(self.validFood.name, "burger")
        self.assertEqual(self.validFood.type, "main course")
        self.assertEqual(self.validFood.description, "delicious")
        self.assertEqual(self.validFood.price, 10.00)
        self.assertEqual(self.validFood.popularity, 3)

    def testValidation(self):
        """
        Tests whether model validation is working as intended.
        """
        invalidName = deepcopy(self.validFood)
        invalidName.name = "thisnameisratherelaboratelylongdon'tyousee?"

        invalidType = deepcopy(self.validFood)
        invalidType.type = "lunch"

        invalidDesc  = deepcopy(self.validFood)
        invalidDesc.description = 100

        invalidPrice = deepcopy(self.validFood)
        invalidPrice.price = "ten"

        invalidPopul = deepcopy(self.validFood)
        invalidPopul.popularity = "nine"

        try:
            self.validFood.clean_fields()
        except Exception as e:
            self.fail("Instantiating the supposed valid object raised "
                      "the following error:\n{}".format(e))

        with self.assertRaises(ValidationError):
            invalidName.clean_fields()
            invalidType.clean_fields()
            invalidDesc.clean_fields()
            invalidPrice.clean_fields()
            invalidPopul.clean_fields()

    def test__str__(self):
        """
        Tests whether the __str__ magic method was override properly.
        """
        self.assertEqual(str(self.validFood), self.validFood.name)


class ViewTests(TestCase):
    """
    Unit tests for the methods in the views file.
    """

    def setUp(self):
        """
        Declares some food and menu data to be used for testing.
        """
        self.foodData = \
        {
            "name": "potato",
            "type": "main course",
            "description": "rather squary...",
            "price": 50,
            "popularity": 3
        }
        self.menuData = {"menu": [self.foodData, self.foodData]}

    @patch("django.core.serializers.serialize")
    def testSendMenu(self, mockSerializeMethod):
        """
        Tests whether the server is able to send a HTTP request back
        successfully upon receiving a request.
        """
        mockRequest = MagicMock()
        mockRequest.method = "GET"
        mockSerializeMethod.return_value = json.dumps(self.menuData)

        response = sendMenu(mockRequest)
        menu = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(menu, self.menuData)

    @patch("menu.tests.Food.objects.create")
    @patch("json.loads")
    def testReceiveMenu(self, mockJsonLoad, mockCreateMethod):
        """
        Tests whether the server is able to receive a menu from the client
        and handle it correctly.
        """
        mockRequest = MagicMock()
        mockRequest.method = "POST"
        mockJsonLoad.return_value = self.menuData

        updateMenu(mockRequest)
        createArgs = [call(**self.foodData), call(**self.foodData)]

        self.assertEqual(mockCreateMethod.call_args_list, createArgs)


############################### INTEGRATION TESTS ##############################


class IntegrationTests(TestCase):
    """
    Integration tests for the menu app.
    """

    def setUp(self):
        """
        Declares some food and menu data to be used for testing.
        """
        self.foodData1 = \
        {
            "name": "potato",
            "type": "main course",
            "description": "rather squary...",
            "price": "50.00",
            "popularity": 3
        }
        self.foodData2 = \
        {
            "name": "cabbage",
            "type": "dessert",
            "description": "rather roundish...",
            "price": "10.00",
            "popularity": 3
        }
        self.menuData = {"menu": [self.foodData1, self.foodData2]}


    def testSendMenuToClient(self):
        """
        Tests whether the server is able to send a json menu to the client
        upon request.
        """
        Food.objects.create(**self.foodData1)
        Food.objects.create(**self.foodData2)

        client = Client()
        response = client.get(reverse("menu-get"))
        data = json.loads(response.content.decode("utf-8"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data[0]["fields"], self.foodData2)
        self.assertEqual(data[1]["fields"], self.foodData1)


    def testReceiveMenuFromClient(self):
        """
        Tests whether the server is able to receive a json menu from the
        client and successfully store it into the database.
        """
        client = Client()
        response = client.post(reverse("menu-update"),
                               json.dumps(self.menuData),
                               content_type="application/json")

        potato = Food.objects.get(name="potato")
        cabbage = Food.objects.get(name="cabbage")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(potato.name, "potato")
        self.assertEqual(cabbage.name, "cabbage")


