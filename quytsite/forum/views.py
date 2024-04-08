from django.http import JsonResponse
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
from django.views import generic
from .models import Posts, Comments


class HomeView(generic.ListView):
    template_name = "forum/home.html"
    context_object_name = "posts_list"

    def get_queryset(self):
        return Posts.objects.all()


class DetailView(generic.DetailView):
    model = Posts
    template_name = "forum/detail.html"


# Create your views here.
