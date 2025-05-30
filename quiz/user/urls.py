from django.urls import path

from user import views

app_name = 'account'


urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register_user'),
    path('profile/', views.profile_user, name='profile_user')
]
