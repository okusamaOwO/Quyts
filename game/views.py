from django.shortcuts import redirect, render
from django.http import HttpResponse
import os
from . models import Room, Question
from django.shortcuts import get_object_or_404
# Create your views here.
from .forms import RoomForm, QuizForm, QuestionForm
from django.contrib.auth.decorators import login_required
from json import dumps 
from .helpers import convert_questions_to_json
from django.http import JsonResponse
from .models import Quiz, Question
import json


def game(request):
    
    return render(request, 'Game.html', context={})

def wait_room(request):
    rooms = Room.objects.all()
    context = {
        'rooms':rooms,
    }
    return render(request, 'room.html', context)

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

def create_quiz(request):
    quiz_form = QuizForm()
    question_form = QuestionForm()
    context = {'quiz_form': quiz_form, 'question_form':question_form}
    if request.method == 'POST':
  
        data = json.loads(request.body)
       
        title = data["quiz_title"]
        description = data["quiz_description"]
        questions = data["questions"]

        
        new_quiz = Quiz.objects.create(title=title, description=description, author = request.user)



        for question in questions:
            question_text = question["text"]
            # Tạo câu hỏi mới và lưu vào quiz
            answer1 = question["answer1"]
            answer2 = question["answer2"]
            answer3 = question["answer3"]
            answer4 = question["answer4"]
            correct_answer = question["corret_answer"]
            question = Question.objects.create(quiz=new_quiz, text=question_text, answer1 = answer1, answer2 = answer2, answer3 = answer3, answer4 = answer4, correct_answer = correct_answer)


        return JsonResponse({'success': True})  # Trả về JSON thành công

    return render(request, 'create_quiz.html', context, )
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



