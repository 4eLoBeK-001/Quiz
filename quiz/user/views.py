from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse

from quiz import settings
from user.forms import LoginUserForm, RegisterUserForm, UploadImageForm
from user.models import Statistics, User


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
    user = request.user
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            user.photo = form.cleaned_data['photo']
            user.save()
            return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = UploadImageForm()
    context = {
        'statistics': statistics,
        'form': form,
        'default_url': settings.MEDIA_URL,
    }
    return render(request, 'user/profile.html', context)
