from django.db import models
from django.contrib.auth.models import User


class DayOfWeek(models.IntegerChoices):
    MONDAY = 1, 'Понедельник'
    TUESDAY = 2, 'Вторник'
    WEDNESDAY = 3, 'Среда'
    THURSDAY = 4, 'Четверг'
    FRIDAY = 5, 'Пятница'
    SATURDAY = 6, 'Суббота'
    SUNDAY = 7, 'Воскресенье'

class Recipe(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название рецепта")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['name']

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients', verbose_name="Рецепт")
    name = models.CharField(max_length=100, verbose_name="Название продукта")
    quantity = models.CharField(max_length=50, verbose_name="Количество")

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return f"{self.name} - {self.quantity}"

class MealPlanner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название блюда")
    description = models.TextField(blank=True, verbose_name="Описание")
    day_of_week = models.IntegerField(choices=DayOfWeek.choices, verbose_name="День недели")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    recipe = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Рецепт")

    class Meta:
        verbose_name = "Планирование меню"
        verbose_name_plural = "Планирование меню"
        ordering = ['day_of_week', 'name']

    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.name}"

class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Ингредиент (из рецепта)"
    )
    custom_item = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Продукт (ручной ввод)"
    )
    custom_quantity = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Количество (ручной ввод)"
    )
    purchased = models.BooleanField(default=False, verbose_name="Куплено")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Список покупок"
        verbose_name_plural = "Список покупок"
        ordering = ['-added_at', 'ingredient__name', 'custom_item']

    def __str__(self):
        if self.ingredient:
            return f"{self.ingredient.name} ({self.ingredient.quantity})"
        else:
            return f"{self.custom_item} ({self.custom_quantity})"