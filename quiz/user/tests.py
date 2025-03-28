from http import HTTPStatus
import random
import string

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from quiz_app.models import Quiz
from .models import Statistics


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class RegisterAuthUserTestCase(TestCase):
    
    def test_register_and_auth(self):
        username = generate_random_string()
        password = generate_random_string()

        path_home = reverse('home')
        data = {
            'username': username,
            'password1': password,
            'password2': password,
        }
        # Проверка регистрации
        register_url = reverse('account:register_user')
        registration_response = self.client.post(register_url, data)
        user = get_user_model().objects.get(username=username)

        self.assertEqual(registration_response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(registration_response, path_home)
        self.assertTrue(user.is_active)

        # Проверка авторизации
        login_url = reverse('account:login_user')
        data = {
            'username': username,
            'password': password
        }
        login_response = self.client.post(login_url, data)

        self.assertEqual(login_response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(login_response, path_home)
        self.assertTrue(self.client.login(username=username, password=password))


class CheckAuthRegisterTestCase(TestCase):

    def setUp(self):
        self.username = 'testUsername'
        self.password = 'testPassword'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)
        self.client.login(username=self.username, password=self.password)
    
        Statistics.objects.create(user=self.user)
    
    def test_page_availability(self):
        """Проверка что нас не будет редиректить"""
        paths = (reverse('create_quiz'), reverse('view_quizzes'), reverse('account:profile_user'))

        for path in paths:
            response = self.client.get(path)
            self.assertEqual(response.status_code, HTTPStatus.OK)