from django.urls import path

from quiz_app import views

urlpatterns = [
    path('home/', views.home, name='home')
]
