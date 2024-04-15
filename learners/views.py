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
            return redirect('learners:index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'learners/login.html')
    