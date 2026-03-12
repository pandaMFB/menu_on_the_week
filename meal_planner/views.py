from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MealPlanner, Recipe, ShoppingList
from .forms import MealPlannerForm, ShoppingListItemForm

@login_required
def index_view(request):
    return render(request, 'meal_planner/index.html')

@login_required
def menu_view(request):
    days = {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье'
    }

    weekly_meals = {
        0: [{'name': 'Омлет', 'description': 'С овощами'}],
        1: [],
    }
    for day_num in range(1, 8):
        weekly_meals[day_num] = MealPlanner.objects.filter(
            user=request.user,
            day_of_week=day_num
        ).order_by('name')
    return render(request, 'menu/menu.html', {
        'days': days,
        'weekly_meals': weekly_meals
    })

@login_required
def recipes_view(request):
    """Страница рецептов (можно доработать позже)."""
    recipes = Recipe.objects.filter(meal__user=request.user).select_related('meal')
    return render(request, 'recipes/recipes.html', {'recipes': recipes})

@login_required
def add_meal_view(request):
    if request.method == 'POST':
        form = MealPlannerForm(request.POST)
        if form.is_valid():
            meal = form.save(commit=False)
            meal.user = request.user
            meal.save()
            messages.success(request, 'Блюдо успешно добавлено!')
            return redirect('meal_planner:menu')
    else:
        form = MealPlannerForm()
    return render(request, 'menu/add_meal.html', {'form': form})

@login_required
def shopping_list_view(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        try:
            item = ShoppingList.objects.get(id=item_id, user=request.user)
            item.purchased = True
            item.save()
        except ShoppingList.DoesNotExist:
            messages.error(request, 'Элемент не найден.')
    items = ShoppingList.objects.filter(user=request.user).order_by('purchased', 'item')
    form = ShoppingListItemForm()
    return render(request, 'shopping/shopping_list.html', {
        'items': items,
        'form': form
    })
