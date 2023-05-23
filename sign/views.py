from datetime import datetime

from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

