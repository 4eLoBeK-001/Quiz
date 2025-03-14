from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.db.models import Count, Max

from quiz import settings
from quiz_app.models import Quiz
from user.forms import LoginUserForm, RegisterUserForm, UploadImageForm
from user.models import Statistics


# Create your views here.


def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request, data=request.POST)
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

@login_required()
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

@login_required()
def profile_user(request):
    user = request.user
    most_popular_quiz = None
    statistics = Statistics.objects.get(user=user)

    if Quiz.objects.filter(author=user).exists():
        popular = Quiz.published.annotate(result_count=Count('results')).filter(author=user)
        most_popular_quiz = popular.order_by('-result_count').first()
    else:
        ...
        
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
        'most_popular_quiz': most_popular_quiz,
        'default_url': settings.MEDIA_URL,
    }
    return render(request, 'user/profile.html', context)
