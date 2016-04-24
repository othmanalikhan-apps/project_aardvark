import json

from django.core import serializers
from django.http import HttpResponse
from .models import Food


def updateMenu(request):
    """
    Receives and stores a menu that is in JSON formatting into the database.
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
    :return: The menu in JSON format.
    """
    if request.method == "GET":
        data = serializers.serialize("json", Food.objects.all())
        return HttpResponse(data, content_type="application/json")