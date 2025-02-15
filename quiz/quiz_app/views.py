from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from quiz_app.forms import CreateQuizForm

# Create your views here.


def home(request):
    return render(request, 'quiz_app/home.html')

@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = CreateQuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.author = request.user
            quiz.save()
            return redirect(reverse('home'))
    else:
        form = CreateQuizForm()

    context = {
        'form': form
    }
    return render(request, 'quiz_app/create_quiz.html', context)
