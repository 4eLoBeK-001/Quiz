from user.models import Statistics


def update_statistics_on_test_completion(request, quiz, user):
    statistic = Statistics.objects.get(user=user)
    difficult = quiz.difficult
    statistic.tests_completed += 1
    if difficult == 'Easy-Quiz':
        statistic.completed_easy_tests += 1
    elif difficult == 'Medium-Quiz':
        statistic.completed_medium_tests += 1
    elif difficult == 'Hard-Quiz':
        statistic.completed_hard_tests += 1
    elif difficult == 'Very-hard-Quiz':
        statistic.completed_very_hard_tests += 1
    statistic.save()


def update_statistics_on_test_creation(request, quiz, user):
    statistic = Statistics.objects.get(user=user)
    difficult = quiz.difficult
    statistic.tests_created += 1
    if difficult == 'Easy-Quiz':
        statistic.easy_tests_created += 1
    elif difficult == 'Medium-Quiz':
        statistic.medium_tests_created += 1
    elif difficult == 'Hard-Quiz':
        statistic.hard_tests_created += 1
    elif difficult == 'Very-hard-Quiz':
        statistic.very_hard_tests_created += 1
    statistic.save()