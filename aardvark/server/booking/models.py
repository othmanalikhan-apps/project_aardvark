import datetime

from django.db import models
from django.contrib import admin
from django.utils.crypto import get_random_string

import string


def _generateID():
    """
    Generates an id number using some random generation.

    :return: A randomly generated reference number.
    """
    refPart1 = get_random_string(3, allowed_chars=string.ascii_uppercase)
    refPart2 = get_random_string(7, allowed_chars=string.digits)
    return refPart1 + refPart2

def _generateUniqueReferenceNumber():
    """
    Generates a unique reference number for the booking.

    :return: A unique reference number.
    """
    while True:
        refNum = _generateID()
        try:
            Booking.objects.get(reference=refNum)
        except Booking.DoesNotExist:
            return refNum


class Booking(models.Model):
    """
    Models for the restaurant bookings

    Attributes:
        :name:          The name of the customer.
        :email:         The email of the customer.
        :phone:         The phone number of the customer
        :date:          The date of the booking.
        :time:          The time of the booking.
        :table:         The table numbers associated with the booking.
        :reference:     The reference number of the booking.
    """
    TIMES = (
        (datetime.time(9, 0), datetime.time(9, 0)),
        (datetime.time(11, 0), datetime.time(11, 0)),
        (datetime.time(13, 0), datetime.time(13, 0)),
        (datetime.time(15, 0), datetime.time(15, 0)),
    )

    name = models.CharField(max_length=50, blank=False)
    email = models.CharField(max_length=80, blank=False)
    phone = models.CharField(max_length=13, blank=False)

    date = models.DateField(blank=False)
    time = models.TimeField(blank=False, choices=TIMES)
    table = models.ForeignKey("table.Table",
                              blank=False,
                              null=True,
                              on_delete=models.SET_NULL)
    reference = models.CharField(max_length=10, blank=False,
                                 default=_generateUniqueReferenceNumber)

    def __str__(self):
        """
        Overriding the built-in python convert to string magic method

        :return: The name of the customer.
        """
        return self.name

    class Meta:
        """
        Meta data for the booking model.
        """
        ordering = ("name",)


class BookingAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "date",
                    "time", "table", "reference")
    ordering = ("date", "time", "name")
    list_per_page = 25

    search_fields = ("name", "email", "phone", "date",
                     "time", "table", "reference")
    list_filter = ("date", "time", "table")
    readonly_fields = ("reference",)
