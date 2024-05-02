from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.topic, name="topic"),
    path("addCard/", views.addCard, name="addCard"),
    path("addTag/", views.addTag, name="addTag"),
    path("delCard/", views.delCard, name="delCard"),
    path("delTag/", views.delTag, name="delTag"),
    path("<str:subject>/", views.tagList, name="tagList"),
    path("<str:subject>/<str:tagname>/", views.flashcardList, name="cardList"),
]
app_name = "flashcards"
