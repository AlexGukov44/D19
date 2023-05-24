import random
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from .models import OneTimeCode


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

def check_code(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username='username', password='password')
    if user is not None:
        OneTimeCode.object.create(code = random.choice('alsjw'), user='user')
        redirect('signup')
    else:
        return HttpResponse('Такой пользователь уже существует')

def login_with_code(request):
    username = request.POST['username']
    code = request.POST['code']
    if OneTimeCode.object.filter(code=code, user__username = 'username').exist():
        login(request, 'user')
    else:
        return HttpResponse('error')



