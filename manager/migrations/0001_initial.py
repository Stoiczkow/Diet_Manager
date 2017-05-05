# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-26 13:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(choices=[(1, 'Breakfast'), (2, 'Second breakfast'), (3, 'Lunch'), (4, 'Dinner'), (5, 'Supper'), (6, 'Other')])),
                ('meal_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=512, null=True)),
                ('calories', models.FloatField()),
                ('category', models.ManyToManyField(to='manager.Category')),
            ],
        ),
        migrations.AddField(
            model_name='meal',
            name='product',
            field=models.ManyToManyField(to='manager.Product'),
        ),
    ]