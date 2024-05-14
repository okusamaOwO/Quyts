from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Room, Quiz,Question

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_code','room_name', 'quiz', 'private']
        
        
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description']
    def __init__(self, *args, **kwargs):
        super(QuizForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
            
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'answer1', 'answer2','answer3','answer4','correct_answer',]
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })