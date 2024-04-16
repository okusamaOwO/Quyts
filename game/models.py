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