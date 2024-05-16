from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm
from .models import Learner
from django.db import IntegrityError

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                learner = Learner.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                )
                return redirect('learners:registration-success')
            except IntegrityError:
                messages.error(request, 'Username already exists!')
                return render(request, 'registration/register.html', {'form': form})
            
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def index(request):
       # Kiểm tra xem người dùng đã đăng nhập hay chưa
    if request.user.is_authenticated:
        # In ra session key của người dùng (session key là một cách duy nhất để xác định session của một người dùng cụ thể)
        print("Session key:", request.session.session_key)
        
        # Lấy thông tin từ session của người dùng
        my_data = request.session.get('my_data_key', 'default_value')
        print("My data from session:", my_data)
    else:
        print("User is not authenticated")
    return render(request, 'learners/index.html')

def registration_success(request):
    return render(request, 'registration/registration_success.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        learner = authenticate(username=username, password=password)
        if learner is not None:
            django_login(request, learner)
            return redirect('flashcards:topic')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'learners/login.html')