from django.contrib import admin

from quiz_app.models import *
# Register your models here.

admin.site.register(Quiz)


admin.site.register(QuizResilt)


@admin.register(Quiestion)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'question_text', 'is_active', 'question_type')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer_text', 'is_correct', 'question')


