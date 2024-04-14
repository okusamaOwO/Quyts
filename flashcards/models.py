from django.db import models
from learners.models import Learner


# Create your models here.
class Cards(models.Model):
    owner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)

    def __str__(self):
        return self.question
