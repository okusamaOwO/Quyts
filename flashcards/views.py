from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Cards, Subject


# Create your views here.
def topic(request):
    return render(request, "flashcards/subject_list.html")


def learnerList(request, subject):
    print(subject)
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


def flashsetList(request, learner):
    print("to be continuee")
    yield