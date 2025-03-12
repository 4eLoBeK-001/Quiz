from django.contrib import admin
from django.contrib.auth import get_user_model

from user.models import Statistics

# Register your models here.

class StatisticTestsCompletedFilter(admin.SimpleListFilter):
    title = 'tests_completed'
    parameter_name = 'tests_completed'

    def lookups(self, request, model_admin):
        return (
            ('25<', 'До 25'),
            ('50<', 'До 50'),
            ('100>', 'От 100')
        )
    
    def queryset(self, request, queryset):
        if self.value() == '25<':
            return queryset.filter(tests_completed__lte=25)
        if self.value() == '50<':
            return queryset.filter(tests_completed__lte=50)
        if self.value() == '100>':
            return queryset.filter(tests_completed__gte=100)


class StatisticsTestsCreatedFilter(admin.SimpleListFilter):
    title = 'test_created'
    parameter_name = 'test_created'

    def lookups(self, request, model_admin):
        return (
            ('25<', 'До 25'),
            ('50<', 'До 50'),
            ('100>', 'От 100')
        )
    
    def queryset(self, request, queryset):
        if self.value() == '25<':
            return queryset.filter(tests_created__lte=25)
        if self.value() == '50<':
            return queryset.filter(tests_created__lte=50)
        if self.value() == '100>':
            return queryset.filter(tests_created__gte=100)



@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    ordering = ('-date_joined',)


@admin.register(Statistics)
class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('user', 'tests_created', 'tests_completed')
    list_filter = (StatisticTestsCompletedFilter, StatisticsTestsCreatedFilter)
    search_fields = ('user__username',)

    fieldsets = (
        (None, {
            'fields': ('user',),
        }),
        ('Tests created', {
            'description': '<h1>Создано тестов</h1>',
            'fields': ('tests_created', 'easy_tests_created', 'medium_tests_created', 'hard_tests_created', 'very_hard_tests_created',),
            'classes': ('collapse',)
        }),
        ('Tests completed', {
            'description': '<h1>Завершено тестов</h1>',
            'fields': ('tests_completed', 'completed_easy_tests', 'completed_medium_tests', 'completed_hard_tests', 'completed_very_hard_tests',),
            'classes': ('collapse',)
        })
    )

