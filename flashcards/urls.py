from django.urls import path, include
from . import views

app_name = "flashcards"
urlpatterns = [
    path("", views.topic, name="topic"),
    path("<str:subject>/", views.learnerList, name="learnerList")
]
