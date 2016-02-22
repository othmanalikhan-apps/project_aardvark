from django.db import models
import time, random

# Create your models here.
class Booking(models.Model):
    """
    Models for the restaurant bookings
    """

    def ref_no(self):
        num = time.strftime("%S%m%M")[::-1]
        str1 = str2 = ""

        for x in range(2):
            str1 += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
            str2 += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

        ref_num = str1 + num + str2

        return ref_num

    reference_no = models.CharField(max_length=10, default=ref_no)
    table = models.ForeignKey('table.Table', on_delete=models.CASCADE)
    customer = models.CharField(max_length=50)
    mobile = models.CharField(max_length=13)
    reserve_date = models.DateTimeField()
    party_size = models.PositiveIntegerField()


    class Meta:
        ordering = ["customer"]