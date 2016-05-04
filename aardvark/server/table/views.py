import json

from django.http import HttpResponse
from .models import Table


#def sendTableSizes(request):
#    """
#    Finds all possible available table sizes from the database then sends
#    the results to the client in JSON format.
#
#    :return: An HTTP response object containing the table sizes.
#    """
#    refNum = {"sizes": ["ERROR"]}
#
#    if request.method == "GET":
#        print("HELLO")
#
#        data = json.loads(request.body.decode("utf-8"))
#
#        print(data)
#        data["table"] = Table.objects.get(number=data["table"])
#        booking = Booking.objects.create(**data)
#        refNum["reference"] = booking.reference
#
#    return HttpResponse(json.dumps(refNum), content_type="application/json")