from django.db import models
from django.contrib import admin


class Table(models.Model):
    """
    Model that represents a food item on the restaurant menu.

    Attributes:
        :number:        The number of the table.
        :size:          The amount of chairs the table has.
        :order:         The order associated with the table.
    """
    number = models.PositiveIntegerField(blank=False)
    size = models.PositiveIntegerField(blank=False)
    order = models.ForeignKey("order.Order",
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name="ordered_table")

    def __str__(self):
        """
        Overriding the built-in python convert to string magic method

        :return: The number of the table.
        """
        return str(self.number)

class TableAdmin(admin.ModelAdmin):
    list_display = ("number", "size",)
    ordering = ("number",)
    list_per_page = 25

    search_fields = ("number", "size")
    list_filter = ("number", "size")
    readonly_fields = ("order",)