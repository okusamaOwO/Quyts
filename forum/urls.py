from django.urls import path
from . import views

app_name = "forum"
urlpatterns = [
    path("", views.homeView, name="home"),
    path("<int:pk>/", views.postView, name="post_detail"),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('dislike/<int:post_id>/', views.dislike_post, name='dislike_post')
]