from django import forms
from .models import MealPlanner, Recipe, ShoppingList


class MealPlannerForm(forms.ModelForm):
    class Meta:
        model = MealPlanner
        fields = ['name', 'description', 'day_of_week', 'recipe']
        labels = {
            'name': 'Название блюда',
            'description': 'Описание',
            'day_of_week': 'День недели',
            'recipe': 'Рецепт (выберите или оставьте пустым)'
        }
        widgets = {
            'day_of_week': forms.Select(choices=MealPlanner._meta.get_field('day_of_week').choices),
            'recipe': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['recipe'].queryset = Recipe.objects.filter(user=user)
        # Название блюда и описание не обязательны, если выбран рецепт
        self.fields['name'].required = False
        self.fields['description'].required = False

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        recipe = cleaned_data.get('recipe')
        if not name and not recipe:
            raise forms.ValidationError('Укажите название блюда или выберите рецепт.')
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.name and instance.recipe:
            instance.name = instance.recipe.name
        if commit:
            instance.save()
        return instance


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['name']
        labels = {'name': 'Название рецепта'}
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}


class ShoppingListItemForm(forms.ModelForm):
    class Meta:
        model = ShoppingList
        fields = ['custom_item', 'custom_quantity']
        labels = {
            'custom_item': 'Продукт',
            'custom_quantity': 'Количество'
        }
        widgets = {
            'custom_item': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: Молоко'}),
            'custom_quantity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1 л'}),
        }