from django.contrib import messages
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.template import loader
from .form import CommentForm, PostForm
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import Post, Comment


def homeView(request):
    posts_list = Post.objects.all()
    template = loader.get_template("forum/home.html")
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            try:
                post = Post.objects.create(
                    post_title=form.cleaned_data['post_title'],
                    post_content=form.cleaned_data['post_content'],
                    pub_date_post=timezone.now(),
                )
                return redirect(reverse("forum:home"))
            except IntegrityError:
                messages.error(request, 'Post error')
    else:
        form = PostForm()
    output = {
        "posts_list": posts_list,
        "form": form,
    }
    return HttpResponse(template.render(output, request))


def postView(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if request.method == "POST":
            form = CommentForm(request.POST)
            if form.is_valid():
                try:
                    comment = post.comment_set.create(
                        comment_context=form.cleaned_data['comment_context'],
                        pub_date_comment=timezone.now(),
                    )
                    return redirect(reverse("forum:post_detail", args=[pk]))
                except IntegrityError:
                    messages.error(request, 'Comment error')
        else:
            form = CommentForm()
    except Post.DoesNotExist:
        raise Http404("Not exist")
    return render(request, "forum/post.html", {"post": post, "form": form})

# Create your views here.
