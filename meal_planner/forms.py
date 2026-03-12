from django import forms
from .models import MealPlanner, ShoppingList, Recipe

class MealPlannerForm(forms.ModelForm):
    class Meta:
        model = MealPlanner
        fields = ['name', 'description', 'day_of_week']
        labels = {
            'name': 'Название блюда',
            'description': 'Описание',
            'day_of_week': 'День недели'
        }
        widgets = {
            'day_of_week': forms.Select(choices=[
                (1, 'Понедельник'),
                (2, 'Вторник'),
                (3, 'Среда'),
                (4, 'Четверг'),
                (5, 'Пятница'),
                (6, 'Суббота'),
                (7, 'Воскресенье'),
            ])
        }

class ShoppingListItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['item', 'quantity']
        labels = {
            'item': 'Продукт',
            'quantity': 'Количество'
        }

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name']
        labels = {
            'name': 'Название рецепта'
        }
