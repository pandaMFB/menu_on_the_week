from django.urls import path
from . import views


app_name = 'meal_planner'

urlpatterns = [
    path('', views.index_view, name='index'),  # Главная страница
    path('menu/', views.menu_view, name='menu'),
    path('recipes/', views.recipes_view, name='recipes'),
    path('add-meal/', views.add_meal_view, name='add_meal'),
    path('shopping/', views.shopping_list_view, name='shopping_list'),
]