from decimal import Decimal
from django.db import models
from django.contrib import admin


class Order(models.Model):
    """
    Model that represents a food item on the restaurant menu.

    Attributes:
        :name:              The name of the food.
        :type:              The type of the food limited to: "starter",
                            "main course", "dessert" and "beverage".
        :description:       The description of the food.
        :price:             The price of the food in GBP.
        :popularity:        The popularity of the food.
    """
    pass


class OrderAdmin(admin.ModelAdmin):
    pass
