from django.urls import path

from quiz_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),

    path('quiz/create/', views.create_quiz, name='create_quiz'),
    path('quiz/mylist/', views.view_quizzes, name='view_quizzes'),
    path('quiz/delete/<int:quiz_id>/', views.delete_quiz, name='delete_quiz'),
    
    path('quiz/<int:quiz_id>/questions', views.list_questions, name='list_questions'),
    path('quiz/<int:quiz_id>/questions/create', views.create_question, name='create_question'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/', views.detail_question, name='detail_question'),
    path('quiz/<int:quiz_id>/question/<int:question_id>/change', views.change_question, name='change_question'),
    
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/result/', views.test_result, name='test_result'),

    path('quiz/list/', views.list_quizzes, name='list_quizzes'),
    path('quiz/<int:quiz_id>/global_statistics/', views.global_statistics, name='global_statistics'),
    path('quiz/list/<int:user_id>/<str:username>', views.user_quizzes, name='user_quizzes'),
]
