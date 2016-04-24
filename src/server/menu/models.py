from decimal import Decimal
from django.db import models
from django.contrib import admin


class Food(models.Model):
    """
    Model that represents a food item on the restaurant menu.
    """
    TYPES = (
        ("starter", "starter"),
        ("main course", "main course"),
        ("dessert", "dessert"),
        ("beverage", "beverage")
    )

    name = models.CharField(max_length=30,
                            blank=False)
    type = models.CharField(max_length=20,
                            choices=TYPES,
                            blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=5,
                                decimal_places=2,
                                blank=False,
                                default=Decimal('0.00'))
    popularity = models.IntegerField(default=0)

    def __str__(self):
        """
        Overriding the built-in python convert to string magic method
        :return: The name of the food object.
        """
        return self.name

    class Meta:
        """
        Meta data for the food model.
        """
        ordering = ["name"]


class MenuAdmin(admin.ModelAdmin):
    """
    Class that changes some parameters to modify the admin interface.
    """
    list_display = ["name", "type", "price"]
    list_per_page = 10
    list_filter = ["name", "type", "price"]
    search_fields = ["name", "type", "description"]
