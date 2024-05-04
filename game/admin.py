from django.contrib import admin

from .models import Room, Quiz, Question
# Register your models here.

admin.site.register(Room)
admin.site.register(Quiz)
admin.site.register(Question)