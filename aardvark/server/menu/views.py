from django.core import serializers
from django.http import HttpResponse
from .models import Food

import json


def updateMenu(request):
    """
    Receives and stores a menu into the database.
    The menu object received is in JSON formatting, specifically in
    the form:

    {"menu" : [food1,
               food2,
               ...,
               foodN]}.

    :param request: A django request object.
    :return: An empty HTTP response object.
    """
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        for foodData in data["menu"]:
            Food.objects.create(**foodData)

    return HttpResponse()

def sendMenu(request):
    """
    Serializes all the data in the Food model, and returns it in JSON
    formatting.

    :param request: A django request object.
    :return: The menu in JSON format.
    """
    if request.method == "GET":
        data = serializers.serialize("json", Food.objects.all())
        return HttpResponse(data, content_type="application/json")