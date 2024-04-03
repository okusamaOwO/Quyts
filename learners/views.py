from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from .forms import RegistrationForm
from .models import Learner

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            learner = Learner.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                is_active=False  # User is inactive until email verification
            )
            # Generate verification token
            token = default_token_generator.make_token(learner)
            # Build verification URL
            domain = get_current_site(request).domain
            verification_url = reverse('verify_email', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(learner.pk)), 'token': token})
            verification_link = f'http://{domain}{verification_url}'
            # Send verification email
            subject = 'Verify your email address'
            message = render_to_string('registration/verification_email.html', {'learner': learner, 'verification_link': verification_link})
            send_mail(subject, message, 'from@example.com', [learner.email])
            return redirect('registration_success')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def index(request):
    return render(request, 'learners/index.html')

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
    