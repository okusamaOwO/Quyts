from django.db import models
from learners.models import Learner


# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Cards(models.Model):
    question = models.CharField(max_length=1000)
    answer = models.CharField(max_length=1000)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    setName = models.CharField(max_length=100, default='Default')
    owner = models.ForeignKey(Learner, on_delete=models.CASCADE)

    def __str__(self):
        return self.question


