from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Cards, Subject
from learners.models import Learner


# Create your views here.
def topic(request):
    return render(request, "flashcards/subject_list.html")


def learnerList(request, subject):
    try:
        subject_querry = Subject.objects.get(name=subject)
    except Subject.DoesNotExist:
        raise Http404("Subject does not exist. You can try finding 'Others' instead")
    else:
        flashcards = Cards.objects.filter(subject_id=subject_querry.id).distinct("owner")
        ownerList = []
        for i in flashcards:
            ownerList += [i.owner]
        context = {
            "ownerList": ownerList,
            "Subject": subject
        }
        return render(request, "flashcards/learner_list.html", context)


def flashsetList(request, subject, username):
    '''
    In this subject, how many flashcard sets does learner have?
    '''
    try:
        owner = Learner.objects.get(username=username)
        subject_querry = Subject.objects.get(name=subject)
    except (Learner.DoesNotExist, Subject.DoesNotExist):
        raise Http404("Not available subject or user")
    else:
        flashcardSet = Cards.objects.filter(owner_id=owner.id, subject_id=subject_querry.id).distinct("setName")
        context = {
            "Subject": subject,
            "owner": owner,
            "flashcardSet": flashcardSet
        }
        return render(request, "flashcards/set_list.html", context)


def flashcardList(request, subject, username, setname):
    try:
        owner = Learner.objects.get(username=username)
        subject_querry = Subject.objects.get(name=subject)
    except (Learner.DoesNotExist, Subject.DoesNotExist):
        raise Http404("Not available subject or user")
    else:
        flashcardSet = Cards.objects.filter(owner_id=owner.id, subject_id=subject_querry.id, setName=setname)
        context = {
            "Subject": subject,
            "owner": owner,
            "flashcardSet": flashcardSet,
            "setName": setname
        }
        return render(request, "flashcards/flashcards.html", context)