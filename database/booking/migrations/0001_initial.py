# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('table', '0004_auto_20160219_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('reference_no', models.PositiveIntegerField(max_length=10)),
                ('customer', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=13)),
                ('reserve_date', models.DateTimeField()),
                ('party_size', models.PositiveIntegerField()),
                ('table', models.ForeignKey(to='table.Table')),
            ],
            options={
                'ordering': ['customer'],
            },
            bases=(models.Model,),
        ),
    ]
