from django.contrib.auth.forms import AuthenticationForm
from django import forms

from user.models import User


class UserLoginForm(AuthenticationForm):

    # username = forms.CharField(
    #     label='Имя',
    #     widget=forms.TextInput(attrs={"autofocus": True,
    #                                   'class': 'form-control',
    #                                   'placeholder': 'Введите ваше имя'}))
    # password = forms.CharField(
    #     label='Пароль',
    #     widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
    #                                       'class': 'form-control',
    #                                       'placeholder': 'Введите ваш пароль'})
    # )

    class Meta:
        model = User
        fields = ['username', 'password']