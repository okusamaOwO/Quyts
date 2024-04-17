from django.db import models
from learners.models import Learner
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.

class Room(models.Model):
    room_code = models.CharField(max_length=20, unique=True)
    room_name = models.CharField(max_length=100)
    host = models.ForeignKey(Learner, related_name='hosted_rooms', on_delete=models.CASCADE)
    participants = models.ManyToManyField(Learner, related_name='joined_rooms')
    start_time = models.DateTimeField(auto_now_add= True)
    
    def __str__(self) -> str:
        return self.room_code
    def get_product_url(self):
      return reverse('room-info', args=[self.slug])
  
class Quiz(models.Model):
    title = models.CharField(max_length=100, default="")
    description = models.TextField(max_length=100, default="")
    author = models.ForeignKey(Learner, on_delete=models.CASCADE)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(max_length=100, default="")
    answer1 = models.CharField(max_length=100, default='')
    answer2 = models.CharField(max_length=100, default='')
    answer3 = models.CharField(max_length=100, default='')
    answer4 = models.CharField(max_length=100, default='')
    correct_answer = models.IntegerField(choices=[(1, 'Answer 1'), (2, 'Answer 2'), (3, 'Answer 3'), (4, 'Answer 4')], default=1)
