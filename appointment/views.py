from django.shortcuts import render
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_managers


# Create your views here.
