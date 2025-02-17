from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from quiz_app.models import Answer, Quiestion, Quiz
from quiz_app.forms import AddAnswerForm, CreateQuestionForm, CreateQuizForm

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
        'questions': questions,
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


def change_question(request, quiz_id, question_id):
    question = get_object_or_404(Quiestion, id=question_id)
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect(reverse('list_questions', args=[quiz_id]))
    else:
        form = CreateQuestionForm(instance=question)
    context = {
        'form': form
    }
    return render(request, 'quiz_app/create_question.html', context)






def delete_question(request, question_id, quiz_id):
    Quiestion.objects.filter(id=question_id, quiz_id=quiz_id).delete()
    return redirect(request.META.get('HTTP_REFERER'))

def detail_question(request, quiz_id, question_id):
    question = get_object_or_404(Quiestion, id=question_id)
    answers = Answer.objects.filter(question=question)

    data_post = request.POST

    if request.method == 'POST':
        if 'save' in data_post:
            answers.update(is_correct=False)
            answer = get_object_or_404(Answer, id=data_post.get('correct_answer'))
            answer.is_correct = True
            answer.save()
            return redirect(request.META.get('HTTP_REFERER'))
        if 'delete' in data_post:
            lo

            return redirect(request.META.get('HTTP_REFERER'))
            

        if 'add-answer' in data_post:
            form = AddAnswerForm(data_post)
            if form.is_valid():
                form = form.save(commit=False)
                form.question = question
                form.save()
                return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = AddAnswerForm()
    context = {
        'form': form,
        'question': question,
        'question_title': question.question_text,
        'answers': answers
    }
    return render(request, 'quiz_app/detail_question.html', context)


def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    answer.delete()
    return redirect(request.META.get('HTTP_REFERER'))
