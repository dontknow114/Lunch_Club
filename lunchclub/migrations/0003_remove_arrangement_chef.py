# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-26 05:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lunchclub', '0002_auto_20171225_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='arrangement',
            name='chef',
        ),
    ]
