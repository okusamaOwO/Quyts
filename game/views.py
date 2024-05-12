from django.shortcuts import redirect, render
from django.http import HttpResponse
import os
from . models import Room, Question
from django.shortcuts import get_object_or_404
# Create your views here.
from .forms import RoomForm
from django.contrib.auth.decorators import login_required
from json import dumps 
from .helpers import convert_questions_to_json

def game(request):
    rooms = Room.objects.all()
    context = {
        'rooms':rooms,
    }
    return render(request, 'Game.html', context)

@login_required
def room(request, room_code):
    room = get_object_or_404(Room, room_code = room_code)
    session= request.session
    
    
    user_name = request.user.username
    quiz_id = room.quiz_id
    host_name = room.host.username
    questions = Question.objects.filter(quiz = quiz_id)
    questions_json = convert_questions_to_json(questions)
    context = {
        'room':room,
        'room_code':room_code,
        'user_name': user_name,
        'session' : session,
        'questions':questions,
        'host_name' : host_name,
        'questions_json' : questions_json,
        
    }
    return render(request, 'lobby.html', context)
@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            form.save()
            return redirect('game') 
    else:
        form = RoomForm()
    return render(request, 'create_room.html', {'form': form})