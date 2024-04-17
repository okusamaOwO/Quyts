from django.urls import path

from . import views

app_name = "learners"
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('registration_success/', views.registration_success, name='registration-success')
]