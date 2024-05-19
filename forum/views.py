import json
from django.contrib import messages
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.template import loader
from .form import CommentForm, PostForm, VoteForm
from django.urls import reverse
from django.views import generic
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Post, Comment
from django.contrib.auth.decorators import login_required


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

@login_required
def postView(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            vote_form = VoteForm(request.POST)
            if comment_form.is_valid():
                try:
                    comment = post.comment_set.create(
                        comment_context=comment_form.cleaned_data['comment_context'],
                        pub_date_comment=timezone.now(),
                    )
                    return redirect(reverse("forum:post_detail", args=[pk]))
                except IntegrityError:
                    messages.error(request, 'Comment error')

                
            data = json.loads(request.body)
            
            if(data["type"] == 'like' ) :
                post.post_like = post.post_like +1
                post.save()
                return JsonResponse({'oke' : "oke"})
            if(data["type"] == 'dislike' ) :
                post.post_dislike = post.post_dislike +1
                post.save()
                return JsonResponse({'oke' : "oke"})
            
            
        else:
            comment_form = CommentForm()
            vote_form = VoteForm()
    except Post.DoesNotExist:
        raise Http404("Not exist")
    return render(request, "forum/post.html", {"post": post, "comment_form": comment_form, "vote_form": vote_form})

@login_required
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.post_like = F('post_like') + 1
    post.save()
    post.refresh_from_db()
    return JsonResponse({'post_like': post.post_like})

@login_required
@require_POST
def dislike_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.post_dislike = F('post_dislike') + 1
    post.save()
    post.refresh_from_db()
    return JsonResponse({'post_dislike': post.post_dislike})

# Create your views here.
