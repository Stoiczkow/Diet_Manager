# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-29 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0003_auto_20170511_1657'),
    ]

    operations = [
        migrations.AddField(
            model_name='meal',
            name='calories',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='carbohydrates',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='fat',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='protein',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='salt',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='meal',
            name='sugars',
            field=models.FloatField(null=True),
        ),
    ]