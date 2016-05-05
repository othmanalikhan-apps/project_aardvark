from django.db import models
from django.contrib import admin


class Order(models.Model):
    """
    Model that represents a order for a table of the restaurant menu.

    Attributes:
        :table:         The table associated with the order.
        :food:          The food item from the restaurant menu associated
                        with the order.
        :quantity:      The amount of food ordered.
    """
    table = models.OneToOneField("table.Table",
                                 blank=False,
                                 null=True,
                                 on_delete=models.SET_NULL,
                                 related_name="table_ordered")
    food = models.OneToOneField("menu.Food",
                                 blank=False,
                                 null=True,
                                 on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        """
        Overriding the built-in python convert to string magic method

        :return: The table number associated with the order.
        """
        return str(self.table.number)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("table", "food")
    ordering = ("table",)
    list_per_page = 25

    search_fields = ("table", "food")
    list_filter = ("table", "food")
