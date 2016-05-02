from django.http import HttpResponse
from .models import Booking
from table.models import Table

import json
import datetime
from copy import deepcopy


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
    :return: An empty HTTP response object.
    """
    refNum = {"reference": "ERROR"}

    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        data["table"] = Table.objects.get(number=data["table"])
        booking = Booking.objects.create(**data)
        refNum["reference"] = booking.reference

    return HttpResponse(json.dumps(refNum), content_type="application/json")

def sendBookingSlots(request, bookingDate):
    """
    Finds the booking slots available for all tables within the table
    database and sends the results to the client. The data sent is a
    dictionary that maps table numbers to a list of times that are two hours
    apart (assumes that a booking slot is 2hrs long):

    {"1": ["14:00", "16:00", "18:00"],
     "2": [],
     "3": ["1:00", "3:00"]}

    :param bookingDate: The date to be searched for booking slots.
    :param request: A django request object.
    :return: An empty HTTP response object.
    """
    freeSlots = {}
    slots = []
    timings = ["9:00", "11:00", "13:00", "15:00"]

    # Generating datetime formatted timings
    for timing in timings:
        slots.append(datetime.datetime.strptime(timing, "%H:%M").time())

    if request.method == "GET":
        # Setting all tables initially to be free at all times
        for table in Table.objects.all():
            freeSlots[table.number] = deepcopy(slots)

        # Searching all the bookings for the given date
        d = datetime.datetime.strptime(bookingDate, '%Y-%m-%d')
        bookings = Booking.objects.filter(date=d.date())

        # Removing slots that are booked
        for booking in bookings:
            freeSlots[booking.table.number].remove(booking.time)

        # Converting datetime to str to allow serializable json
        for key in freeSlots.keys():
            freeSlots[key] = [slot.strftime("%H:%M") for slot in freeSlots[key]]

        data = json.dumps(freeSlots)
        return HttpResponse(data, content_type="application/json")







