from django.contrib import admin
from .models import Food, FoodAdmin

admin.site.register(Food, FoodAdmin)
