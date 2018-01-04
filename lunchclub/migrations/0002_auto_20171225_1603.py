# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-26 00:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lunchclub', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chef',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='chef',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='chef',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]