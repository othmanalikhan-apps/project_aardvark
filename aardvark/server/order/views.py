from django.http import HttpResponse
from .models import Order
from table.models import Table
from menu.models import Food

import json


def updateOrder(request):
    """
    Receives order data in JSON formatting and stores it into the database.
    The ordered data received is in JSON formatting, specifically in the
    form:

    {"order": [{"table": number,
               "food": name,
               "quantity": number},

               {"table": number,
               "food": name,
               "quantity": number}]}

    :param request: A django request object.
    :return: An empty HTTP response object.
    """
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        for order in data["order"]:
            table = Table.objects.get(number=order["table"])
            food = Food.objects.get(name=order["food"])
            quantity = order["quantity"]
            Order.objects.create(table=table, food=food, quantity=quantity)

    return HttpResponse()

