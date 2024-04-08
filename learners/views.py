from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.urls import reverse
from .forms import RegistrationForm
from .models import Learner
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
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
                return redirect('registration_success')
            except IntegrityError:
                messages.error(request, 'Username already exists!')
                return render(request, 'registration/register.html', {'form': form})
            
    else:
        form = RegistrationForm()
    return render(request, 'registration/r gister.html', {'form': form})


def index(request):
    return render(request, 'learners/index.html')

def registration_success(request):
    return render(request, 'learners/registration_success.html')

def registration_failed(request):
    return render(request, 'learners/registration_failed.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        learner = authenticate(username=username, password=password)
        if learner is not None:
            login(request, learner)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'learners/login.html')
    