from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from quiz_app.models import Quiz


def user_is_quiz_creator(view_func):
    '''Декоратор ограничивает доступ к редактирования тестов, созданных не им'''
    def wrapper(request, quiz_id, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        if request.user != quiz.author:
            return HttpResponseForbidden('Нет права')
        return view_func(request, quiz_id, *args, **kwargs)
    return wrapper