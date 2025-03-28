from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Quiz
from user.models import Statistics

# Create your tests here.

class TestingUrlTestCase(TestCase):

    def test_main_page(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'quiz_app/home.html')

    def test_redirect_url(self):
        """Тест проверяющий редирект для неавторизованного пользователя"""
        redirect_url = '/account/login/?next='
        paths = (reverse('create_quiz'), reverse('view_quizzes'), reverse('account:profile_user'))

        for path in paths:
            response = self.client.get(path)
            self.assertEqual(response.status_code, HTTPStatus.FOUND)
            self.assertRedirects(response, f'{redirect_url}{path}')

class CheckCreateReadDeleteQuizOperations(TestCase):
    
    def setUp(self):
        self.username = 'testUsername'
        self.password = 'testPassword'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)

        Statistics.objects.create(user=self.user)
    
    def test_create_and_delete_quiz(self):
        """Тест создания и удаления викторины"""
        post_data = {
            'name': 'Викторина 2',
            'description': 'Описание викторины 2',
            'difficult': 'Medium-Quiz',
            'is_show': 'on'
        }
        path = reverse('create_quiz')
        response = self.client.post(path, data=post_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertURLEqual(response.url, '/quiz/1/questions')

        # Проверка существования викторины
        quiz = Quiz.objects.get(author=self.user)
        self.assertIsNotNone(quiz)

        # Проверяем, что викторина создалась с правильными данными
        self.assertEqual(quiz.name, 'Викторина 2')
        self.assertEqual(quiz.description, 'Описание викторины 2')
        self.assertEqual(quiz.difficult, 'Medium-Quiz')
        self.assertEqual(quiz.is_show, True)

        # Проверка удаления викторины
        path = reverse('delete_quiz', args=[quiz.id])
        response = self.client.post(path)
        self.assertFalse(Quiz.objects.filter(author=self.user))