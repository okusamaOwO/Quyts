from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader

from django.urls import reverse
from .models import Cards, Subject, Tag

from learners.models import Learner
from django.contrib.auth.decorators import login_required


# Create your views here.
def topic(request):
    return render(request, "flashcards/subject_list.html")


def tagList(request, subject):
    try:
        subject = Subject.objects.get(name=subject)
    except Subject.DoesNotExist:
        raise Http404("Not available subject")
    else:
        tags = subject.tag_set.all()
        context = {
            "tags": tags,
            "Subject": subject.name,
        }
        return render(request, "flashcards/tag_list.html", context)


def flashcardList(request, subject, tagname):
    try:
        tag = Tag.objects.get(name=tagname)
        owner = tag.owner
    except (Learner.DoesNotExist, Tag.DoesNotExist):
        raise Http404("Not available tag or user")
    else:
        flashcardList = tag.cards_set.all()
        context = {
            "Subject": subject,
            "owner": owner,
            "flashcardList": flashcardList,
            "tag": tag
        }
        return render(request, "flashcards/flashcards.html", context)


@login_required
def addCard(request):
    owner = request.user
    tags = owner.tag_set.all()

    if request.method == 'POST':
        question = request.POST["question"]
        answer = request.POST["answer"]
        tagName = request.POST["tagName"]

        if not tagName or not question or not answer:
            return render(
                request,
                "flashcards/add_cards.html",
                {
                    "error_message": "Don't leave a blank",
                    "tags": tags,
                }
            )
        else:
            tag = Tag.objects.get(name=tagName)
            tag.cards_set.create(question=question, answer=answer)
            return HttpResponseRedirect(reverse("flashcards:addCard") + "?inform_message=Submitted successfully")
    else:
        inform_message = request.GET.get("inform_message")
        return render(request, "flashcards/add_cards.html", {"tags": tags, "inform_message": inform_message,})


@login_required
def addTag(request):
    owner = request.user
    subjects = Subject.objects.all()

    if request.method == 'POST':
        subject = request.POST["subject"]
        tagName = request.POST["tagName"]
        if not subject or not tagName:
            return render(
                request,
                "flashcards/add_tag.html",
                {
                    "error_message": "Don't leave a blank",
                    "subjects": subjects,
                }
            )
        else:
            subject = Subject.objects.get(name=subject)
            subject.tag_set.create(name=tagName, owner_id=owner.id)
            return HttpResponseRedirect(
                reverse("flashcards:addCard") +
                "?inform_message=Create a new set successfully. Add some cards to your set.")
    else:
        return render(request, "flashcards/add_tag.html", {"subjects": subjects,})


@login_required
def delTag(request):
    owner = request.user
    tags = owner.tag_set.all()

    if request.method == 'POST':
        tagName = request.POST["tagName"]
        if not tagName:
            return render(
                request,
                "flashcards/del_tag.html",
                {
                    "error_message": "Don't leave a blank",
                    "tags": tags,
                }
            )
        else:
            tag = Tag.objects.get(name=tagName)
            tag.delete()
            return HttpResponseRedirect(reverse("flashcards:delTag") + "?inform_message=Done")
    else:
        inform_message = request.GET.get("inform_message")
        return render(request, "flashcards/del_tag.html", {"tags": tags, "inform_message": inform_message})


@login_required
def delCard(request):
    owner = request.user
    tags = owner.tag_set.all()

    if request.method == 'POST':
        question = request.POST["question"]
        answer = request.POST["answer"]
        tagName = request.POST["tagName"]

        if not tagName or not question or not answer:
            return render(
                request,
                "flashcards/del_cards.html",
                {
                    "error_message": "Don't leave a blank",
                    "tags": tags,
                }
            )
        else:
            try:
                tag = Tag.objects.get(name=tagName)
                card = tag.cards_set.get(question=question, answer=answer)
            except Cards.DoesNotExist:
                return render(
                    request,
                    "flashcards/del_cards.html",
                    {
                        "error_message": "No available cards fit",
                        "tags": tags,
                    }
                )
            else:
                card.delete()
                return HttpResponseRedirect(reverse("flashcards:delCard") + "?inform_message=Done")
    else:
        inform_message = request.GET.get("inform_message")
        return render(request, "flashcards/del_cards.html", {"tags": tags, "inform_message": inform_message, })