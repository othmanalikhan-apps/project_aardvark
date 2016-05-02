from django.contrib import admin
from .models import Booking, BookingAdmin

admin.site.register(Booking, BookingAdmin)
