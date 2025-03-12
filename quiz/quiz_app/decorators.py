from django.shortcuts import get_object_or_404, render
from quiz_app.models import Quiz


def user_is_quiz_creator(view_func):
    '''Декоратор ограничивает доступ к редактирования тестов, для посторонних'''
    def wrapper(request, quiz_id, *args, **kwargs):
        quiz = get_object_or_404(Quiz, id=quiz_id)
        if request.user != quiz.author:
            details = {
                'datails': 'Вы не можете как-либо изменять(редактировать) тесты созданные не вами'
            }
            return render(request, '403.html', context=details, status=403)
        return view_func(request, quiz_id, *args, **kwargs)
    return wrapper