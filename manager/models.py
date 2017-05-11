from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    @property
    def category_name(self):
        return "{}".format(self.name)

    def __str__(self):
        return self.category_name

    def get_absolute_url(self):
        return reverse("list_category")


class Product(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=512, null=True)
    calories = models.FloatField(null=True)
    carbohydrates = models.FloatField(null=True)
    protein = models.FloatField(null=True)
    sugars = models.FloatField(null=True)
    salt = models.FloatField(null=True)
    fat = models.FloatField(null=True)
    category = models.ManyToManyField(Category)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    @property
    def product_name(self):
        return "{}".format(self.name)

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse("list_product")


class Meal(models.Model):
    name = models.IntegerField(choices=MEAL_NAME)
    product = models.ManyToManyField(Product, through='Quantity')
    meal_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    @property
    def meal_name(self):
        meal_name_dict = dict(MEAL_NAME)
        return "{}".format(meal_name_dict[self.name])

    def __str__(self):
        return self.meal_name

    def get_absolute_url(self):
        return reverse("list_meal")


class Quantity(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()