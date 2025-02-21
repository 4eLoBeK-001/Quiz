from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.timezone import now

from quiz_app.statistics import update_statistics_on_test_completion, update_statistics_on_test_creation
from quiz_app.models import Answer, Question, Quiz, QuizResult
from quiz_app.forms import AddAnswerForm, CreateQuestionForm, CreateQuizForm


# Create your views here.


def home(request):
    return render(request, 'quiz_app/home.html')



def create_quiz(request):
    if request.method == 'POST':
        form = CreateQuizForm(request.POST)
        if form.is_valid():
            user = request.user
            quiz = form.save(commit=False)
            quiz.author = user
            update_statistics_on_test_creation(request, quiz, user)
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
    questions = Question.objects.filter(quiz=quiz)

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
    question = get_object_or_404(Question, id=question_id)
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
    Question.objects.filter(id=question_id, quiz_id=quiz_id).delete()
    return redirect(request.META.get('HTTP_REFERER'))

def detail_question(request, quiz_id, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question)

    data_post = request.POST

    if request.method == 'POST':
        if 'save' in data_post:
            if question.question_type == 'single':
                selected_answer = get_object_or_404(Answer, id=data_post.get('correct_answer'))
                answers.update(is_correct=False)
                selected_answer.is_correct = True
                selected_answer.save()
            elif question.question_type == 'multiple':
                selected_answers = data_post.getlist('correct_answer')
                answers.update(is_correct=False)
                for id_selected_answers in selected_answers:
                    Answer.objects.filter(id=id_selected_answers).update(is_correct=True)
            return redirect(request.META.get('HTTP_REFERER'))
        
        if 'delete' in data_post:
            selected_answer = get_object_or_404(Answer, id=data_post.get('delete'))
            selected_answer.delete()
            if not answers.filter(is_correct=True).exists():  # Если нет верных ответов
                answer_first = answers.first()
                answer_first.is_correct = True
                answer_first.save()
            return redirect(request.META.get('HTTP_REFERER'))
            
        if 'add-answer' in data_post:
            form = AddAnswerForm(data_post)
            if form.is_valid():
                form = form.save(commit=False)
                form.question = question
                if not question.answers.exists():  # Если это первый ответ
                    form.is_correct=True
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


def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)
    number_questions = questions.count()
    user=request.user

    if number_questions > 0:
        if request.method == 'POST':
            score = 0
            start_time_str = request.session.get('quiz_start_time')
            start_time = datetime.fromisoformat(start_time_str)
            end_time = now()

            for question in questions:
                if question.question_type == 'single':
                    correct_answer = question.answers.get(is_correct=True)
                    selected_answer = request.POST.get(str(correct_answer.question_id))
                    if str(correct_answer.id) == selected_answer:
                        score += 1

                elif question.question_type == 'multiple':
                    correct_answers = question.answers.filter(is_correct=True)
                    selected_answers = request.POST.getlist(str(question.id))
                    lst_correct_answers = [str(answer.id) for answer in correct_answers]

                    if set(lst_correct_answers) == set(selected_answers):
                        score += 1

                elif question.question_type == 'input-text':
                    correct_answer = question.answers.get(is_correct=True)
                    filled_field = request.POST.get(str(correct_answer.question_id))
                    if correct_answer.answer_text == filled_field:
                        score += 1

            percentage = (score/ questions.count()) * 100 # Процент верных ответов

            result = {
                'user': user,
                'quiz': quiz,
                'correct_answers': score,
                'total_questions':number_questions,
                'percentage': round(percentage, 2),
                'time_taken': round((end_time - start_time).total_seconds(), 1),
                'completed_at': end_time,
            }
            if not user.is_anonymous:
                QuizResult.objects.create(**result)
                update_statistics_on_test_completion(request, quiz, user)
                return test_result(request, quiz, user)
            else:
                result = {'quiz_result': result}
                return render(request, 'quiz_app/quiz_result.html', result)

        
        else:
            request.session['quiz_start_time'] = now().isoformat()
            context = {
                'quiz': quiz,
                'questions': questions,
            }
            return render(request, 'quiz_app/take_quiz.html', context)
    
    else:
        messages.warning(request, message='Вы не создали ни одного вопроса')
        return redirect(reverse('list_questions', args=[quiz_id]))


def test_result(request, quiz, user):
    quiz_result = QuizResult.objects.filter(quiz=quiz, user=user).latest('completed_at')
    context = {
        'quiz_result': quiz_result
    }
    return render(request, 'quiz_app/quiz_result.html', context)
