# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_auto_20160220_0021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='reference_no',
            field=models.CharField(max_length=10, default='hi'),
            preserve_default=True,
        ),
    ]
