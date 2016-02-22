from django.db import models

# Create your models here.
class Order(models.Model):
	'''Models for the restaurant order'''

	table = models.ForeignKey("table.Table", on_delete = models.CASCADE)
	meal = models.ForeignKey("menu.Menu", related_name='Name', on_delete = models.CASCADE)
	quantity = models.PositiveIntegerField()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["table"]
