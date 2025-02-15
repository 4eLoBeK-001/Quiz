from django.contrib import admin

from quiz_app.models import *
# Register your models here.

admin.site.register(Quiz)

admin.site.register(Quiestion)

admin.site.register(Answer)

admin.site.register(QuizResilt)
