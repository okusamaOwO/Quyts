from django.shortcuts import render
from django.http import HttpResponse
import os
from . models import Room
from django.shortcuts import get_object_or_404
# Create your views here.

def game(request):
    rooms = Room.objects.all()
    context = {
        'rooms':rooms,
    }
    return render(request, 'Game.html', context)

def room(request, room_code):
    print(room_code)
    room = get_object_or_404(Room, room_code = room_code)
    context = {
        'room':room,
    }
    return render(request, 'lobby.html', context)