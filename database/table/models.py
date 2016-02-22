from django.db import models
from django.contrib import admin

# Create your models here.
class Table(models.Model):
	'''Models for the restaurant table'''

	table = models.PositiveIntegerField()
	book = models.BooleanField(default=False)

	def __str__(self):
		return str(self.table)

	class Meta:
		ordering = ["table"]

	@property
	def Available(self):
		return "Table %s is already booked" % self.table if self.book == True else "Table %s is free" % self.table

	def Booked(self):
		return True if self.book == True else False

	Booked.boolean = True


class TableAdmin(admin.ModelAdmin):
	list_display = ["table", "Available", "Booked"]
	list_per_page = 10
	list_filter = ["book"]