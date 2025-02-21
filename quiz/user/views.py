from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse

from user.forms import LoginUserForm, RegisterUserForm
from user.models import Statistics

# Create your views here.


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                login(request, user)
                return redirect(reverse('home'))
    else:
        form = LoginUserForm()
    
    context = {
        'form': form
    }
    return render(request, 'user/login.html', context)


def logout_user(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            Statistics.objects.create(user=user)
            return redirect(reverse('home'))
    else:
        form = RegisterUserForm()
    
    context = {
        'form': form
    }

    return render(request, 'user/register.html', context)


def profile_user(request):
    statistics = Statistics.objects.get(user=request.user)
    context = {
        'statistics': statistics
    }
    return render(request, 'user/profile.html', context)