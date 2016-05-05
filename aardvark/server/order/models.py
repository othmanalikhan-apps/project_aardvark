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
        :isHistory:     Boolean that indicates whether the order has expired
                        (used for distinguishing between fresh orders and
                        orders from history)
    """
    table = models.ForeignKey("table.Table",
                              blank=False,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name="TABLE_ORDERED",
                              unique=False)
    food = models.ForeignKey("menu.Food",
                             blank=False,
                             null=True,
                             on_delete=models.SET_NULL,
                             unique=False)
    quantity = models.PositiveIntegerField(blank=False, null=False)
    isHistory = models.BooleanField(blank=False, null=False, default=False)
    isPaid = models.BooleanField(blank=False, null=False, default=False)

    def __str__(self):
        """
        Overriding the built-in python convert to string magic method

        :return: The table number associated with the order.
        """
        return str(self.table.number)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("table", "food", "quantity", "isHistory", "isPaid")
    ordering = ("isHistory", "table")
    list_per_page = 25

    search_fields = ("table", "food", "quantity")
    list_filter = ("table", "food", "quantity")
