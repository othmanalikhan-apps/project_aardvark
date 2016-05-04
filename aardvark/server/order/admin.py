from django.contrib import admin
from .models import Order,OrderAdmin 

admin.site.register(Order, OrderAdmin)
