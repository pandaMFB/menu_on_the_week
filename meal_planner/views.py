from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MealPlanner, Recipe, ShoppingList
from .forms import MealPlannerForm, RecipeForm, ShoppingListItemForm


@login_required
def index_view(request):
    return render(request, 'meal_planner/index.html')


@login_required
def menu_view(request):
    days = {
        1: 'Понедельник',
        2: 'Вторник',
        3: 'Среда',
        4: 'Четверг',
        5: 'Пятница',
        6: 'Суббота',
        7: 'Воскресенье'
    }

    weekly_meals = {}
    for day_num in range(1, 8):
        meals = MealPlanner.objects.filter(user=request.user, day_of_week=day_num).select_related('recipe')
        weekly_meals[day_num] = meals
    return render(request, 'menu/menu.html', {'days': days, 'weekly_meals': weekly_meals})


@login_required
def recipes_view(request):
    recipes = Recipe.objects.filter(user=request.user).prefetch_related('ingredients')
    return render(request, 'recipes/recipes.html', {'recipes': recipes})


@login_required
def add_meal_view(request):
    if request.method == 'POST':
        form = MealPlannerForm(request.POST, user=request.user)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            # Если выбран рецепт, добавляем его ингредиенты в список покупок
            if meal.recipe:
                for ing in meal.recipe.ingredients.all():
                    ShoppingList.objects.get_or_create(
                        user=request.user,
                        ingredient=ing,
                        defaults={'purchased': False}
                    )
            messages.success(request, 'Блюдо успешно добавлено в меню!')
            return redirect('meal_planner:menu')
        else:
            messages.error(request, 'Ошибка при добавлении блюда.')
    else:
        form = MealPlannerForm(user=request.user)
    return render(request, 'menu/add_meal.html', {'form': form})


@login_required
def add_recipe_view(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            messages.success(request, 'Рецепт добавлен. Теперь можно добавить ингредиенты.')
            return redirect('meal_planner:recipes')
        else:
            messages.error(request, 'Ошибка при добавлении рецепта.')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})


@login_required
def shopping_list_view(request):
    if request.method == 'POST':
        if 'item_id' in request.POST:
            # Отметка купленного
            item_id = request.POST.get('item_id')
            try:
                shopping_item = ShoppingList.objects.get(id=item_id, user=request.user)
                shopping_item.purchased = True
                shopping_item.save()
                messages.success(request, 'Продукт отмечен купленным.')
            except ShoppingList.DoesNotExist:
                messages.error(request, 'Элемент не найден.')
        else:
            # Ручное добавление продукта
            form = ShoppingListItemForm(request.POST)
            if form.is_valid():
                new_item = form.save(commit=False)
                new_item.user = request.user
                new_item.save()
                messages.success(request, 'Продукт добавлен в список покупок.')
            else:
                messages.error(request, 'Ошибка при добавлении продукта.')
        return redirect('meal_planner:shopping_list')

    items = ShoppingList.objects.filter(user=request.user).select_related('ingredient').order_by('purchased', 'ingredient__name', 'custom_item')
    form = ShoppingListItemForm()
    return render(request, 'shopping/shopping_list.html', {'items': items, 'form': form})


@login_required
def shopping_list_view(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            shopping_item = ShoppingList.objects.get(id=item_id, user=request.user)
            shopping_item.purchased = True
            shopping_item.save()
            messages.success(request, 'Продукт отмечен купленным.')
        except ShoppingList.DoesNotExist:
            messages.error(request, 'Элемент не найден.')
        return redirect('meal_planner:shopping_list')

    items = ShoppingList.objects.filter(user=request.user).select_related('ingredient').order_by('purchased', 'ingredient__name')
    return render(request, 'shopping/shopping_list.html', {'items': items})
