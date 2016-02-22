# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import booking.models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_auto_20160220_0022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='reference_no',
            field=models.CharField(max_length=10, default=booking.models.Booking.ref_no),
            preserve_default=True,
        ),
    ]
