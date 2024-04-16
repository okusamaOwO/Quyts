from . import views
from django.urls import path


urlpatterns = [
    path('game/', views.game, name = 'game'),
    path('game/<str:room_code>/',views.room, name= 'rooms'),
]
