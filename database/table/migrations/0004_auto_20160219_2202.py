# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0003_table_booked'),
    ]

    operations = [
        migrations.RenameField(
            model_name='table',
            old_name='booked',
            new_name='book',
        ),
    ]
