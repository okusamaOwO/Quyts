from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Cards, Subject


# Create your views here.
def topic(request):
    return render(request, "flashcards/topic.html")


def detailSubject(request, subject):
    flashcards = Cards.objects.all().distinct("owner")
    owners = []
    for i in flashcards:
        owners += [i.owner]
    yield
