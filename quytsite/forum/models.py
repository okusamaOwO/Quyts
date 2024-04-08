import datetime
from datetime import timezone
from django.db import models

class Posts(models.Model):
    title = models.CharField(max_length=50)
    context = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Comments(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    context = models.CharField(max_length=100)

    def __str__(self):
        return self.context
# Create your models here.
