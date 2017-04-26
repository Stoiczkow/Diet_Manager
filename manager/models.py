from django.db import models
from django.contrib.auth.models import User
# Create your models here.

MEAL_NAME = (
    (1, "Breakfast"),
    (2, "Second breakfast"),
    (3, "Lunch"),
    (4, "Dinner"),
    (5, "Supper"),
    (6, "Other")
)


class Category(models.Model):
    name = models.CharField(max_length=128)


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, null=True)
    calories = models.FloatField()
    category = models.ManyToManyField(Category)


class Meal(models.Model):
    name = models.IntegerField(choices=MEAL_NAME)
    product = models.ManyToManyField(Product)
    meal_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)