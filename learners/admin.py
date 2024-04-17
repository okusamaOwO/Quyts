from django.contrib import admin
from game.models import Room, Question, Quiz
from learners.models import Learner


admin.site.register(Room)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Learner)