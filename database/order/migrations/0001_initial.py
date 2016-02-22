# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
        ('table', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField()),
                ('meal', models.ForeignKey(to='menu.Menu', related_name='Name')),
                ('table', models.ForeignKey(to='table.Table')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
