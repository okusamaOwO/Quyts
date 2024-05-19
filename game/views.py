from django.shortcuts import redirect, render
from django.http import HttpResponse
import os
from .models import Room, Question
from django.shortcuts import get_object_or_404
# Create your views here.
from .forms import RoomForm, QuizForm, QuestionForm
from django.contrib.auth.decorators import login_required
from json import dumps
from .helpers import convert_questions_to_json
from django.http import JsonResponse
from .models import Quiz, Question
from flashcards.models import Tag, Cards
import json
import google.generativeai as genai
from django.core import serializers


def game(request):
    return render(request, 'game/Game.html', context={})


def wait_room(request):
    rooms = Room.objects.all()
    rooms_json = serializers.serialize('json', rooms)
    context = {
        'rooms': rooms,
        'rooms_json' : rooms_json,
    }
    return render(request, 'game/room.html', context)


@login_required
def room(request, room_code):
    room = get_object_or_404(Room, room_code=room_code)
    session = request.session

    user_name = request.user.username
    quiz_id = room.quiz_id
    host_name = room.host.username
    questions = Question.objects.filter(quiz=quiz_id)
    questions_json = convert_questions_to_json(questions)
    context = {
        'room': room,
        'room_code': room_code,
        'user_name': user_name,
        'session': session,
        'questions': questions,
        'host_name': host_name,
        'questions_json': questions_json,

    }
    return render(request, 'game/lobby.html', context)


def create_quiz(request):
    context = {}
    if request.method == 'POST':

        data = json.loads(request.body)

        title = data["quiz_title"]
        description = data["quiz_description"]
        questions = data["questions"]

        new_quiz = Quiz.objects.create(title=title, description=description, author=request.user)

        for question in questions:
            question_text = question["text"]
   
            answer1 = question["answer1"]
            answer2 = question["answer2"]
            answer3 = question["answer3"]
            answer4 = question["answer4"]
            correct_answer = question["correct_answer"]
            question = Question.objects.create(quiz=new_quiz, text=question_text, answer1=answer1, answer2=answer2,
                                               answer3=answer3, answer4=answer4, correct_answer=correct_answer)

        return JsonResponse({'success': True})  

    return render(request, 'game/create_quiz.html', context, )


@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            form.save()
            return redirect('game:game')
    else:
        form = RoomForm()
    return render(request, 'game/create_room.html', {'form': form})


@login_required
def create_flashcard_quiz(request):
    owner = request.user
    try:
        tags = owner.tag_set.all()
    except:
        print("you dont have tag")
    context = {'tags': tags}

    if request.method == 'POST':

        data = json.loads(request.body)

        title = data["quiz_title"]

        tag_name = data["tag_name"]
        tag = get_object_or_404(Tag, name=tag_name)
        description = data["quiz_description"]
        flashcards = Cards.objects.filter(tag=tag.id)
        print(type(flashcards))
        genai.configure(api_key="AIzaSyCFAZdIrub6t8x5EsUfIZ8wFMd2J_UxfHo")
        model = genai.GenerativeModel('models/gemini-1.0-pro')
        questions = []
        for flashcard in flashcards:
            try:
                front = flashcard.question
                back = flashcard.answer
                prompt = f"""
                Generate a multiple-choice question from a flashcard in the specified language:
                - Front side: {front} (string)
                - Back side: {back} (string)
                - Language: English

                Return a JSON object (have to same)  in the following format ():
                {{
                    "text": "{{question text}}", (string)
                    "answers": ["answer1", "answer2", "answer3", "answer4"], (list of strings)
                    "correct_answer": {{index of correct answer}} (integer)
                }}
                
                """
                response = model.generate_content(prompt)
                print(response.text)
                question = json.loads(response.text)
                questions.append(question)
            except:
                pass

        new_quiz = Quiz.objects.create(title=title, description=description, author=request.user)

        for question in questions:
            try :
                question_text = question["text"]
                # Tạo câu hỏi mới và lưu vào quiz
                answer1 = question["answers"][0]
                answer2 = question["answers"][1]
                answer3 = question["answers"][2]
                answer4 = question["answers"][3]
                correct_answer = question["correct_answer"]
                question = Question.objects.create(quiz=new_quiz, text=question_text, answer1=answer1, answer2=answer2,
                                                answer3=answer3, answer4=answer4, correct_answer=correct_answer)
            except:
                pass
        return JsonResponse({'success': True})  # Trả về JSON thành công
    return render(request, 'game/quiz_flashcard.html', context, )


