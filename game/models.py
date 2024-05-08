from django.db import models
from learners.models import Learner
from django.urls import reverse
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
# Create your models here.
from learners.contextprocessers import get_user


class Quiz(models.Model):
    title = models.CharField(max_length=100, default="")
    description = models.TextField(max_length=100, default="")
    author = models.ForeignKey(Learner, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Room(models.Model):
    room_code = models.CharField(max_length=20, unique=True)
    room_name = models.CharField(max_length=100)
    host = models.ForeignKey(Learner, related_name='hosted_rooms', on_delete=models.CASCADE, default= None )
    participants = models.ManyToManyField(Learner, related_name='joined_rooms', null = True)
    start_time = models.DateTimeField(auto_now_add= True)
    quiz = models.ForeignKey(Quiz, on_delete= models.CASCADE, default= "1", null= True)
    private = models.BooleanField(default= True)
    
    def __str__(self) -> str:
        return self.room_code
    def get_product_url(self):
      return reverse('room-info', args=[self.slug])
    
    def add_participant(room_code,learner):
        room = get_object_or_404(Room,room_code = room_code)
        room.participants.add(learner)
        
    def remove_participant(room_code,learner):
        room = get_object_or_404(Room,room_code = room_code)
        try:
            room.participants.remove(learner)
        except:
            print('loi roi')
    
    def get_number_participants(room_code):
        room = get_object_or_404(Room,room_code = room_code)
        count = room.participants.count()
        return count

        


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    title = models.TextField(max_length=100, default="")
    text = models.TextField(max_length=100, default="")
    answer1 = models.CharField(max_length=100, default='')
    answer2 = models.CharField(max_length=100, default='')
    answer3 = models.CharField(max_length=100, default='')
    answer4 = models.CharField(max_length=100, default='')
    correct_answer = models.IntegerField(choices=[(0, 'Answer 1'), (1, 'Answer 2'), (2, 'Answer 3'), (3, 'Answer 4')], default=0)
    def __str__(self):
        return self.title
