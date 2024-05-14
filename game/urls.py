from . import views
from django.urls import path


urlpatterns = [
    path('', views.game, name = 'game'),
    path('room/play/<str:room_code>/',views.room, name= 'room'),
    path('room/create_room/',views.create_room, name = 'create-room'),
    path('quiz/create_quiz/', views.create_quiz, name = 'create-quiz'),
    path('quiz/create_quiz_from_flashcard/', views.create_flashcard_quiz, name = 'quiz-flashcard'),
    path('room/', views.wait_room, name = 'rooms')
]



