from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from quiz_app.models import Quiestion, Quiz
from quiz_app.forms import CreateQuestionForm, CreateQuizForm

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


def view_quizzes(request):
    quizzes = Quiz.objects.all()

    context = {
        'quizzes': quizzes
    }
    return render(request, 'quiz_app/mylist_quizzes.html', context)


def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def list_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Quiestion.objects.filter(quiz=quiz)

    context = {
        'quiz': quiz,
        'questions': questions
    }
    return render(request, 'quiz_app/list_questions.html', context)


def create_question(request, quiz_id):
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.quiz_id = quiz_id
            form.save()
            return redirect(reverse('list_questions', args=[quiz_id]))
    else:
        form = CreateQuestionForm()

    context = {
        'form': form
    }
    return render(request, 'quiz_app/create_question.html', context)


def delete_question(request, question_id, quiz_id):
    Quiestion.objects.filter(id=question_id, quiz_id=quiz_id).delete()
    return redirect(request.META.get('HTTP_REFERER'))