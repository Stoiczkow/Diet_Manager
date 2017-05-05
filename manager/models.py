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

    @property
    def category_name(self):
        return "{}".format(self.name)

    def __str__(self):
        return self.category_name


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, null=True)
    calories = models.FloatField()
    category = models.ManyToManyField(Category)

    @property
    def product_name(self):
        return "{}".format(self.name)

    def __str__(self):
        return self.product_name

class Meal(models.Model):
    name = models.IntegerField(choices=MEAL_NAME)
    product = models.ManyToManyField(Product)
    meal_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)