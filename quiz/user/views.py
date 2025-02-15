from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse

from user.forms import LoginUserForm, RegisterUserForm

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

