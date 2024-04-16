from django.urls import path, include
from . import views

app_name = "flashcards"
urlpatterns = [
    path("", views.topic, name="topic"),
    path("<str:subject>/", views.learnerList, name="learnerList"),
    path("<str:subject>/<str:username>", views.flashsetList, name="setList"),
    path("<str:subject>/<str:username>/<str:setname>", views.flashcardList, name="cardList")
]
