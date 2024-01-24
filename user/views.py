from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from user.forms import UserLoginForm, UserRegistrationForm, ProfileForm


# Create your views here.


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт")
                redirect_page = request.POST.get('next')
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(redirect_page)

                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'Home - Логин',
        'form': form
    }
    return render(request, 'user/login.html', context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            messages.success(request, f"{user.username}, Вы успешно зарегистрировались")
            if request.POST.get('next'):
                return HttpResponseRedirect(request.POST['next'])
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'Home - Регистрация',
        'form': form
    }
    return render(request, 'user/registration.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль обновлен")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)
    context = {
        'title': 'Home - Кабинет',
        'form': form
    }
    return render(request, 'user/profile.html', context)


@login_required
def logout(request):
    auth.logout(request)
    messages.success(request, f'{request.user.username} Вы вышли из аккаунта')
    return redirect(reverse('main:index'))


def users_cart(request):
    return render(request, "user/users_cart.html")
