from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

class PublishedQuizManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_show=True)

class DraftQuizManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_show=False)


class Quiz(models.Model):
    EASY = 'Easy-Quiz'
    MEDIUN = 'Medium-Quiz'
    HARD = 'Hard-Quiz'
    VERY_HARD = 'Very-hard-Quiz'

    QUIZ_DIFFICULT = [
        (EASY, 'Лёгкая'),
        (MEDIUN, 'Средняя'),
        (HARD, 'Тяжёлая'),
        (VERY_HARD, 'Очень сложная'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    difficult = models.CharField(max_length=20, choices=QUIZ_DIFFICULT, default=EASY)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='quiz')
    created_at = models.DateTimeField(auto_now_add=True)
    is_show = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created_at']
    
    objects = models.Manager()
    published = PublishedQuizManager()
    draft = DraftQuizManager()



class Question(models.Model):
    SINGLE_CHOICE = 'single'
    MULTIPLE_CHOICE = 'multiple'
    TEXT_INPUT = 'input-text'

    QUESTION_TYPES = [
        (SINGLE_CHOICE, 'Одиночный выбор ответа'),
        (MULTIPLE_CHOICE, 'Множественный выбор ответов'),
        (TEXT_INPUT, 'Ввод текста'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(max_length=40, choices=QUESTION_TYPES)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question_text
    
    class Meta:
        ordering = ['id']


class Answer(models.Model):
    answer_text = models.CharField(max_length=120)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return self.answer_text


class QuizResult(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='quiz_results')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='results')
    correct_answers = models.PositiveIntegerField(help_text='Верных ответов')
    total_questions = models.PositiveIntegerField(help_text='Количество вопросов')
    percentage = models.FloatField(help_text='Процент правильных ответов')
    time_taken = models.FloatField(help_text='Время выполнения в секундах')
    completed_at = models.DateTimeField()
    
    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f'{self.user} выполнил {self.quiz.name} на ({self.percentage}%)'
    