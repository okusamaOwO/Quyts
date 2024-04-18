from django.shortcuts import redirect, render
from django.http import HttpResponse
import os
from . models import Room
from django.shortcuts import get_object_or_404
# Create your views here.
from .forms import RoomForm
from django.contrib.auth.decorators import login_required

def game(request):
    rooms = Room.objects.all()
    context = {
        'rooms':rooms,
    }
    return render(request, 'Game.html', context)

@login_required
def room(request, room_code):
    room = get_object_or_404(Room, room_code = room_code)
    
        # Lấy session của người dùng
    session= request.session
    
    # Kiểm tra xem người dùng đã được tạo session key chưa, nếu chưa, tạo mới
    
    user = request.user
    context = {
        'room':room,
        'room_code':room_code,
        'user': user,
        'session' : session,
        
    }
    return render(request, 'lobby.html', context)
@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('game') 
    else:
        form = RoomForm()
    return render(request, 'create_room.html', {'form': form})