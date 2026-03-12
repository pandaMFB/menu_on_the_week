from django.db import models
from django.contrib.auth.models import User

class MealPlanner(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    day_of_week = models.IntegerField()  # 1-7 (Пн-Вс)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    meal = models.ForeignKey(MealPlanner, on_delete=models.CASCADE)

class ShoppingList(models.Model):
    item = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchased = models.BooleanField(default=False)

