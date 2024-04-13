from django.db import models

class Post(models.Model):
    post_title = models.CharField(max_length=200)
    post_content = models.CharField(max_length=400)
    post_like = models.IntegerField(default=0)
    post_dislike = models.IntegerField(default=0)
    pub_date_post = models.DateTimeField("date published")

    def __str__(self):
        return self.post_title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_context = models.CharField(max_length=200)
    comment_like = models.IntegerField(default=0)
    comment_dislike = models.IntegerField(default=0)
    pub_date_comment = models.DateTimeField("date published")

    def __str__(self):
        return self.comment_context

# Create your models here.
