
from django.shortcuts import render, redirect
from django.contrib import messages
# from .models import Contact
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

def home_screen_view(request):
	print(request.headers)
	return render(request, "index.html", {})

def privacy_screen_view(request):
	print(request.headers)
	return render(request, "privacy.html", {})

def condition_screen_view(request):
	print(request.headers)
	return render(request, "terms.html", {})

def evaluation_screen_view(request):
	print(request.headers)
	return render(request, "eval.html", {})