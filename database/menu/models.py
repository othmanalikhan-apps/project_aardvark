from django.db import models
from django.contrib import admin

# Create your models here.
class Menu(models.Model):
	'''Models for the restaurant menu'''

	name = models.CharField(max_length = 30)
	description = models.TextField()
	price = models.DecimalField(max_digits=5, decimal_places=2, null = True)

	def __str__(self):
		return self.name

	@property
	def Price(self):
		return "£%.2f" % self.price if self.price else ""

	class Meta:
		ordering = ["name"]

class MenuAdmin(admin.ModelAdmin):
	list_display = ["name", "Price"]
	list_per_page = 10
	list_filter = ["name", "price"]
	search_fields = ["name", "description"]