from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    photo = models.ImageField(upload_to='user/profile_pictures/%Y/%m/%d/', verbose_name='avatar')


class Statistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='statistics')
    
    tests_created = models.IntegerField(default=0)
    easy_tests_created = models.IntegerField(default=0)
    medium_tests_created = models.IntegerField(default=0)
    hard_tests_created = models.IntegerField(default=0)
    very_hard_tests_created = models.IntegerField(default=0)
    
    tests_completed = models.IntegerField(default=0)
    completed_easy_tests = models.IntegerField(default=0)
    completed_medium_tests = models.IntegerField(default=0)
    completed_hard_tests = models.IntegerField(default=0)
    completed_very_hard_tests = models.IntegerField(default=0)

    def __str__(self):
        return f'Статистика для {self.user.username}'
