from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.topic, name="topic"),
    path("add/<str:username>", views.addCard, name="add"),
    path("<str:subject>/", views.learnerList, name="learnerList"),
    path("<str:subject>/<str:username>", views.flashsetList, name="setList"),
    path("<str:subject>/<str:username>/<str:setname>", views.flashcardList, name="cardList"),
]
app_name = "flashcards"
