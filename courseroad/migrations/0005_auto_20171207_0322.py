# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-07 03:22
from __future__ import unicode_literals

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('courseroad', '0004_auto_20171207_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucket',
            name='json',
            field=picklefield.fields.PickledObjectField(editable=False),
        ),
    ]
