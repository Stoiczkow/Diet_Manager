# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-09 13:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quantity',
            name='unit',
        ),
    ]
