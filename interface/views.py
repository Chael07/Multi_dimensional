
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail
from .models import Household



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

def result_screen_view(request):
	print(request.headers)
	return render(request, "result.html", {})

def login(request):
	print(request.headers)
	return render(request, "admin-login.html", {})

def officials_dashboard_screen_view(request):
    print(request.headers)
    return render(request, "dashboard.html", {})

def officials_table_screen_view(request):
    print(request.headers)
    return render(request, "table.html", {})


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


# views.py

def submit_household(request):
    if request.method == 'POST':
        q1 = float(request.POST.get('q1', 0))
        q2 = float(request.POST.get('q2', 0))
        q3 = float(request.POST.get('q3', 0))
        q4 = float(request.POST.get('q4', 0))
        q5 = float(request.POST.get('q5', 0))
        q6 = float(request.POST.get('q6', 0))
        q7 = float(request.POST.get('q7', 0))
        q8 = float(request.POST.get('q8', 0))
        q9 = float(request.POST.get('q9', 0))
        q10 = float(request.POST.get('q10', 0))
        q11 = float(request.POST.get('q11', 0))
        q12 = float(request.POST.get('q12', 0))
        q13 = float(request.POST.get('q13', 0))

        # Calculate MPI
        MPI = (q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9 + q10 + q11 + q12 + q13) * 100

        # Create Household object with MPI
        Household.objects.create(
        q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, q6=q6,
        q7=q7, q8=q8, q9=q9, q10=q10, q11=q11, q12=q12, q13=q13, mpi=MPI
        )


        return redirect('result')  # Replace 'result' with the actual URL or name of the success page
    
    else:
        return render(request, 'eval.html')
    

