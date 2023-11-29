
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
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

	
def submit_contact_form(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        message = request.POST.get('message')

         # Save to the database
        contact_model_instance = Contact(first_name=first_name, email=email, message=message)
        contact_model_instance.save()

        # Send email to the developer
        subject = 'New Feedback Submission'
        message_body = f"Name: {first_name}\nEmail: {email}\nMessage: {message}"

        # Change the recipient email address to the actual developer's email
        recipient_email = '202080469@psu.palawan.edu.ph'

        send_mail(subject, message_body, email, [recipient_email])
        messages.success(request, 'Form submitted successfully!')
        return redirect('home')  # Redirect to a success page or wherever you want
    else:
        # Handle GET request or other methods if needed
        return render(request, 'index.html')

