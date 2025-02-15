from django.urls import path

from quiz_app import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('quiz/create/', views.create_quiz, name='create_quiz')
]
