from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from accounts.forms import LoginForm, RegisterForm


def login_view(request):
    """Страница входа /accounts/login/"""
    if request.user.is_authenticated:
        return redirect('meal_planner:index')

    if request.method == 'POST':
        form =  LoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Добро пожаловать, {user.username}!")
            return redirect('meal_planner:index')
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def home_view(request):
    return render(request, 'accounts/home.html')


def logout_view(request):
    logout(request)
    messages.info(request, "Вы вышли из системы.")
    return redirect('accounts:login')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Регистрация успешна!")
            return redirect('meal_planner:index')
        else:
            # Собираем все ошибки
            errors = []
            for field, err_list in form.errors.items():
                for err in err_list:
                    errors.append(str(err))
            messages.error(request, "Ошибка регистрации!")
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
