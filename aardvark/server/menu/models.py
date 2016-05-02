from decimal import Decimal
from django.db import models
from django.contrib import admin


class Food(models.Model):
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
                                default=Decimal("0.00"))
    popularity = models.PositiveIntegerField(default=0)

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
        ordering = ("name",)


class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "price", "popularity")
    ordering = ("type", "name")
    list_per_page = 25

    search_fields = ("name", "type", "description", "price", "popularity")
    list_filter = ("type", "price", "popularity")
    readonly_fields = ("popularity",)
