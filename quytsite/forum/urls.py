from django.urls import path
from . import views

app_name = 'forum'
urlpatterns = [
    path("home/", views.HomeView.as_view(), name='home'),
    path("home/<int:pk>/", views.DetailView.as_view(), name='detail'),
]