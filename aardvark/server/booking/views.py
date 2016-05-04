from django.http import HttpResponse
from .models import Booking
from table.models import Table

import json
from datetime import datetime


def updateBooking(request):
    """
    Receives booking data in JSON formatting and stores it into the database.
    The menu object received is in JSON formatting, specifically in the
    form:

    {"booking" : {"name": value1,
                  "phone": value2,
                  "email": value3,
                  "date": value4,
                  "time": value5,
                  "table": value6}}.

    :param request: A django request object.
    :return: An HTTP response object containing the reference number.
    """
    refNum = {"reference": "ERROR"}

    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))

        booking = {"name": data["name"],
                   "email": data["email"],
                   "phone": data["phone"],
                   "date": data["date"],
                   "time": data["time"],
                   "table": Table.objects.filter(number=data["table"])[0] }

        booking = Booking.objects.create(**booking)
        refNum["reference"] = booking.reference

    return HttpResponse(json.dumps(refNum), content_type="application/json")

def sendBookingSizes(request):
    """
    Searches the database by date and then time for all available table sizes
    then returns the results as an HTTP object.

    :param request: A django request object.
    :return: An HTTP response object containing the booking slots.
    """
    if request.method == "GET":
        date = datetime.strptime(request.GET["date"], "%Y-%m-%d").date()
        time = datetime.strptime(request.GET["time"], "%H:%M").time()
        bookings = Booking.objects.filter(date=date, time=time)

        bookedTables = []
        for booking in bookings:
            bookedTables.append(booking.table)

        sizes = []
        for table in Table.objects.all():
            if table not in bookedTables:
                sizes.append(str(table.size))

        freeSlots = {"sizes": sizes}
        data = json.dumps(freeSlots)
        return HttpResponse(data, content_type="application/json")


def sendBookingTables(request):
    """
    Searches the database by date, time and size for all available tables
    then returns the results as an HTTP object.

    :param request: A django request object.
    :return: An HTTP response object containing the booking slots.
    """
    if request.method == "GET":
        date = datetime.strptime(request.GET["date"], "%Y-%m-%d").date()
        time = datetime.strptime(request.GET["time"], "%H:%M").time()
        bookings = Booking.objects.filter(date=date, time=time)

        bookedTables = []
        for booking in bookings:
            bookedTables.append(booking.table)

        tables = []
        size = int(request.GET["size"])
        for table in Table.objects.all():
            if table not in bookedTables and table.size == size:
                tables.append(str(table.number))

        freeSlots = {"tables": tables}
        data = json.dumps(freeSlots)
        return HttpResponse(data, content_type="application/json")






