from django.urls import path
from . import views

app_name = "forum"
urlpatterns = [
    path("", views.homeView, name="home"),
    path("<int:pk>/", views.postView, name="post_detail")
]