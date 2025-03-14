import smtplib

from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Avg, Q
from django.urls import reverse
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.core.mail import send_mail

from quiz import settings
from quiz_app.decorators import user_is_quiz_creator
from quiz_app.statistics import update_statistics_on_test_completion, update_statistics_on_test_creation
from quiz_app.models import Answer, Question, Quiz, QuizResult
from quiz_app.forms import AddAnswerForm, ContactForm, CreateQuestionForm, CreateQuizForm



def home(request):
    return render(request, 'quiz_app/home.html')

def about(request):
    return render(request, 'quiz_app/about.html')

def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            full_message = (
                    f'''Имя: {name} \n
                    Email: {email} \n
                    Сообщение: {message}''')
            try:
                send_mail(
                    subject='Новое сообщение с сайта',
                    message=full_message,
                    from_email=email,
                    recipient_list=['grandinkv@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, message='Сообщение успешно отправлено')
                return redirect(reverse('home'))

            except smtplib.SMTPAuthenticationError as e:
                request.session['email_error_context'] = {
                    'name': name,
                    'email': email,
                    'message': message,
                    'error': str(e),
                    'detail': 'Скорее всего вы не настроили правильно переменные "EMAIL_HOST_USER" и "EMAIL_HOST_PASSWORD"'
                }
                raise Exception('Скорее всего вы не настроили правильно переменные "EMAIL_HOST_USER" и "EMAIL_HOST_PASSWORD"')

    else:
        form = ContactForm()
    
    context = {
        'form': form
    }
    return render(request, 'quiz_app/contacts.html', context)

@login_required()
def create_quiz(request):
    if request.method == 'POST':
        form = CreateQuizForm(request.POST)
        if form.is_valid():
            user = request.user
            quiz = form.save(commit=False)
            quiz.author = user
            update_statistics_on_test_creation(request, quiz, user)
            quiz.save()
            return redirect(reverse('list_questions', args=[quiz.id]))
    else:
        form = CreateQuizForm()

    context = {
        'form': form
    }
    return render(request, 'quiz_app/create_quiz.html', context)

@login_required()
def view_quizzes(request):
    quizzes = Quiz.objects.filter(author=request.user)

    context = {
        'quizzes': quizzes
    }
    return render(request, 'quiz_app/mylist_quizzes.html', context)


@login_required()
@user_is_quiz_creator
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required()
@user_is_quiz_creator
def list_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz)

    if request.method == 'POST':
        if 'is_show' in request.POST:
            quiz.is_show = not quiz.is_show
            quiz.save()
        else:
            quiz.is_show = not quiz.is_show
            quiz.save()

    context = {
        'quiz': quiz,
        'questions': questions,
    }
    return render(request, 'quiz_app/list_questions.html', context)

@login_required()
@user_is_quiz_creator
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

@login_required()
@user_is_quiz_creator
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

@login_required()
@user_is_quiz_creator
def delete_question(request, question_id, quiz_id):
    Question.objects.filter(id=question_id, quiz_id=quiz_id).delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required()
@user_is_quiz_creator
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
            elif question.question_type == 'input-text':
                save_write_input = request.POST['save-write-input']
                answers.update(answer_text=save_write_input)
            return redirect(request.META.get('HTTP_REFERER'))
        
        if 'delete' in data_post:
            selected_answer = get_object_or_404(Answer, id=data_post.get('delete'))
            selected_answer.delete()
            if not answers.exists():
                return redirect(request.META.get('HTTP_REFERER'))
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

@login_required()
@user_is_quiz_creator
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    answer.delete()
    return redirect(request.META.get('HTTP_REFERER'))


def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz, is_active=True)
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
    elif number_questions == 0:
        messages.warning(request, message='Вы не создали ни одного вопроса')
        return redirect(reverse('list_questions', args=[quiz_id]))


def test_result(request, quiz, user):
    quiz_result = QuizResult.objects.filter(quiz=quiz, user=user).latest('completed_at')
    context = {
        'quiz_result': quiz_result
    }
    return render(request, 'quiz_app/quiz_result.html', context)


def list_quizzes(request):
    quizzes = Quiz.objects.annotate(
        active_questions_count=Count('questions', filter=Q(questions__is_active=True))
        ).filter(is_show=True, active_questions_count__gte=1)
    

    sorting_method = request.POST.get('sort', 'random')

    if request.method == 'POST':
        if sorting_method == 'random':
            quizzes = quizzes.order_by('?') # Работает только для PostgreSQL
        elif sorting_method == 'newest':
            quizzes = quizzes.order_by('-created_at')
        elif sorting_method == 'most_questions':
            quizzes = quizzes.order_by('-active_questions_count')
        elif sorting_method == 'least_questions':
            quizzes = quizzes.order_by('active_questions_count')


    per_page = request.GET.get('paginate_by', 10)
    page_number = request.GET.get('page')

    paginator = Paginator(quizzes, per_page)
    page_obj = paginator.get_page(page_number)

    context = {
        'quizzes': page_obj
    }
    return render(request, 'quiz_app/list_quizzes.html', context)



def global_statistics(request, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz.objects
        .annotate(
            total_count=Count('results'),
            avg_score=Avg('results__percentage'),
            avg_time=Avg('results__time_taken')
        ), id=quiz_id
    )

    questions_count = quiz.questions.filter(is_active=True)
    last_test = quiz.results.latest('completed_at').completed_at.date() if quiz.results.exists() else 'Нет прохождений'
    
    if not user.is_anonymous:
        histories = QuizResult.objects.filter(user=request.user, quiz_id=quiz_id)
    else:
        histories = ''

    context = {
        'quiz': quiz,
        'questions_count': questions_count.count(),
        'created_at': quiz.created_at,
        'last_test': last_test,
        'histories': histories
    }
    return render(request, 'quiz_app/global_statistics.html', context)


def user_quizzes(request, user_id, username):
    user = get_object_or_404(get_user_model(), id=user_id, username=username)
    quizzes = Quiz.objects.annotate(
        active_questions_count=Count('questions', filter=Q(questions__is_active=True))
        ).filter(author=user, is_show=True, active_questions_count__gte=1)

    context = {
        'user': user,
        'username': user.username,
        'quizzes': quizzes,
        'default_url': settings.MEDIA_URL
    }
    return render(request, 'quiz_app/list_user_quizzes.html', context)


