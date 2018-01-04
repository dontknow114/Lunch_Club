# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-25 23:53
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Arrangement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular transaction for this lunch instance', primary_key=True, serialize=False)),
                ('serve_date', models.DateField(blank=True, null=True)),
                ('kudos_amount', models.IntegerField(help_text='Amount for this transaction')),
                ('serve_status_chef', models.CharField(blank=True, choices=[('P', 'Planned'), ('S', 'Served'), ('C', 'Cancelled'), ('D', 'Disputed')], default='P', help_text='Status of the lunch provided', max_length=1)),
                ('serve_status_gastronome', models.CharField(blank=True, choices=[('R', 'Reserved'), ('V', 'Received'), ('C', 'Cancelled'), ('D', 'Disputed')], default='R', help_text='Status of the lunch reserved', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Chef',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('user', models.OneToOneField(default='Jamison', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Lunch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lunchname', models.CharField(max_length=200)),
                ('description', models.TextField(help_text='Enter a brief description of the lunch', max_length=1000)),
                ('chef', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lunchclub.Chef')),
            ],
        ),
        migrations.CreateModel(
            name='LunchInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular lunch across all lunches served and planned', primary_key=True, serialize=False)),
                ('information', models.TextField(max_length=1000)),
                ('serve_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('po', 'Planned Open'), ('pc', 'Planned Closed'), ('sd', 'Served'), ('cd', 'Cancelled')], default='po', help_text='Status of the Lunch Instance', max_length=2)),
                ('lunch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lunchclub.Lunch')),
            ],
            options={
                'ordering': ['serve_date'],
            },
        ),
        migrations.CreateModel(
            name='NutritionCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the nutritional category for the Lunch.', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='lunch',
            name='nutritioncategory',
            field=models.ManyToManyField(help_text='Select a nutrition category for this book', to='lunchclub.NutritionCategory'),
        ),
        migrations.AddField(
            model_name='arrangement',
            name='chef',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chef_arrangement', to='lunchclub.Chef'),
        ),
        migrations.AddField(
            model_name='arrangement',
            name='gastronome',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gastronome_arrangement', to='lunchclub.Chef'),
        ),
        migrations.AddField(
            model_name='arrangement',
            name='lunchinstance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lunchclub.LunchInstance'),
        ),
    ]