from django.contrib import admin

from quiz_app.models import *
# Register your models here.

def change_status(modeladmin, request, queryset, status):
    if queryset.model == Quiz:
        queryset.update(is_show=status)
    if queryset.model == Question:
        queryset.update(is_active=status)
def make_published(modeladmin, request, queryset):
    change_status(modeladmin, request, queryset, True)
def make_unpublished(modeladmin, request, queryset):
    change_status(modeladmin, request, queryset, False)


make_published.short_description = 'Отметить выбранные как опубликованные'
make_unpublished.short_description = 'Отметить выбранные как неопубликованные'

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficult', 'author', 'created_at', 'is_show')
    ordering = ('-created_at',)
    list_filter = ('difficult', 'is_show',)
    search_fields = ('name', 'author__username')

    actions = (make_published, make_unpublished)

    fields = ('name', 'description', 'difficult', 'author', 'created_at', 'is_show')
    readonly_fields = ('created_at', 'author')



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_text', 'question_type', 'is_active')
    list_filter = ('question_type', 'is_active')
    search_fields = ('quiz', 'question_text')

    actions = (make_published, make_unpublished)

    fields = ('quiz', 'question_text', 'question_type', 'is_active')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer_text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('question',)

    fields = ('answer_text', 'question', 'is_correct')


@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz','correct_answers', 'total_questions', 'formatted_percentage', 'completed_at')
    list_display_links = ('user', 'quiz')
    ordering = ('-completed_at',)

    fields = ('user', 'quiz', 'correct_answers', 'total_questions', 'percentage', 'completed_at')
    readonly_fields = ('user', 'quiz', 'correct_answers', 'total_questions', 'percentage', 'completed_at')
    
    def formatted_percentage(self, obj):
        return f'{obj.percentage:.1f}%'
    
    formatted_percentage.short_description = 'percentage'

    # def has_add_permission(self, request):
    #     return False