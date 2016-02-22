# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0002_auto_20160219_1923'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='booked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
