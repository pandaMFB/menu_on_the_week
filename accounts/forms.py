from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите логин',
            'class': 'form-control',
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль',
            'class': 'form-control',
        })
    )

    def get_user(self):
        """
        Метод для аутентификации пользователя.
        Возвращает объект User, если логин/пароль верны, иначе None.
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        return authenticate(username=username, password=password)


class RegisterForm(forms.ModelForm):
    # Кастомные поля (нет в модели User)
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'class': 'form-control'
        }),
        min_length=8,
        error_messages={
            'min_length': 'Пароль должен быть не короче 8 символов.'
        }
    )

    confirm_password = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Подтверждение пароля',
            'class': 'form-control'
        }),
        min_length=8,
        error_messages={
            'min_length': 'Пароль должен быть не короче 8 символов.'
        }
    )

    class Meta:
        model = User
        fields = ['username', 'email']  # Только поля из модели

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Логин',
                'class': 'form-control',
                'pattern': r'^[a-zA-Z][a-zA-Z0-9@$_!#]*$',
                'title': 'Логин должен начинаться с буквы и может содержать буквы, цифры и символы @$_!#'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email',
                'class': 'form-control'
            })
        }

        error_messages = {
            'username': {
                'min_length': 'Имя пользователя должно быть не короче 3 символов.',
                'max_length': 'Имя пользователя не может превышать 16 символов.',
                'required': 'Это поле обязательно для заполнения.',
            },
            'email': {
                'required': 'Это поле обязательно для заполнения.'
            }
        }

    def clean_username(self):
        username = self.cleaned_data['username']

        # 1. Проверка на запрещённые значения
        if not username or username.strip().lower() in ('none', 'null', ''):
            raise ValidationError('Недопустимое значение для логина.')

        # 2. Начинается с буквы
        if not re.match(r'^[a-zA-Z]', username):
            raise ValidationError('Логин должен начинаться с буквы.')

        # 3. Разрешённые символы
        if not re.match(r'^[a-zA-Z0-9@$_!#]+$', username):
            raise ValidationError('Разрешены только латинские буквы, цифры и символы: @$_!#')

        # 4. Хотя бы одна буква
        if not re.search(r'[a-zA-Z]', username):
            raise ValidationError('Логин должен содержать хотя бы одну латинскую букву.')

        # 5. Нет пробелов/табуляции
        if re.search(r'\s', username):
            raise ValidationError('Пробелы и табуляция запрещены.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Проверка совпадения паролей
        if password != confirm_password:
            raise ValidationError('Пароли не совпадают.')

        # Дополнительные проверки пароля
        if password:
            if not re.search(r'\d', password):
                raise ValidationError('Пароль должен содержать хотя бы одну цифру.')
            if not re.search(r'[a-zA-Z]', password):
                raise ValidationError('Пароль должен содержать хотя бы одну букву.')


        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user