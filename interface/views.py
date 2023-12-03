
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth import logout

from .models import Household
from .models import Contact
from .models import Contact_Developer

def home_screen_view(request):
	print(request.headers)
	return render(request, "index.html", {})

def privacy_screen_view(request):
	print(request.headers)
	return render(request, "privacy.html", {})

def evaluation_screen_view(request):
	print(request.headers)
	return render(request, "eval.html", {})

def result_screen_view(request):
	print(request.headers)
	return render(request, "result.html", {})

def login_acc(request):
	print(request.headers)
	return render(request, "admin-login.html", {})

def officials_dashboard_screen_view(request):
    print(request.headers)
    contact_data_set = Contact.objects.all().order_by('-submission_time')[:5]
    poor_count_dt, non_poor_count_dt, poor_count_svm, non_poor_count_svm = get_poor_non_poor_counts()
    return render(request, "user-admin/dashboard.html", 
        {'contact_data_set': contact_data_set, 
        'poor_count_dt': poor_count_dt,
        'non_poor_count_dt': non_poor_count_dt,
        'poor_count_svm': poor_count_svm,
        'non_poor_count_svm': non_poor_count_svm,
         })

def get_poor_non_poor_counts():
    # Fetch data from the Household model
    household_data = Household.objects.values('q1', 'q2')

    # Initialize counters
    poor_count_dt = 0
    non_poor_count_dt = 0
    poor_count_svm = 0
    non_poor_count_svm = 0

    # Count based on the values of q1, q2, q3, and q4
    for record in household_data:
        if record['q1'] == 0.076923077:
            poor_count_dt += 1
        else:
            non_poor_count_dt += 1

    for record in household_data:
        if record['q2'] == 0.076923077:
            poor_count_svm += 1
        else:
            non_poor_count_svm += 1

        # Similar counting logic for SVM, adjust as needed based on your conditions
    return poor_count_dt, non_poor_count_dt, poor_count_svm, non_poor_count_svm


def officials_table_screen_view(request):
    print(request.headers)
    household_data = Household.objects.values('q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13').order_by('id')
    
    converted_household_data = []
    for record in household_data:
        converted_record = {key: convert_to_yes_no(value) for key, value in record.items()}
        converted_household_data.append(converted_record)

    print(converted_household_data)
    return render(request, "user-admin/table.html", {'household_data': converted_household_data})

def convert_to_yes_no(value):
    if value == 0.076923077:
        return 'yes'
    elif value == 0.0:
        return 'no'
    else:
        return 'none'


def officials_addacc_screen_view(request):
    print(request.headers)
    return render(request, "user-admin/add-acc.html", {})

def forgot_pass_screen_view(request):
    print(request.headers)
    return render(request, "admin-forgotpass.html", {})


def add_account_form(request):
    if request.method == "POST":
        Adminfname = request.POST['fname']
        Adminlname = request.POST['lname']
        AdminUsername = request.POST['Username']
        AdminEmail = request.POST['Admin-email']
        AdminPass1 = request.POST['password1']
        AdminPass2 = request.POST['password2']

        # Check if passwords match
        if AdminPass1 != AdminPass2:
            messages.error(request, "Passwords do not match.")
            return redirect('AddAcc')

        # Create the user with the correct arguments
        myadmin = User.objects.create_user(AdminUsername, AdminEmail, password=AdminPass1)
        myadmin.first_name = Adminfname 
        myadmin.last_name = Adminlname
        myadmin.save()

        messages.success(request, "Your account has been successfully created.")
        return redirect('AddAcc')
    
def login_account_form(request):
    if request.method == 'POST':
        loginUsername = request.POST['Username']
        password1 = request.POST['password1']

        user = authenticate(username=loginUsername, password=password1)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Check if the username exists in the database
            user_with_username = User.objects.filter(username=loginUsername).exists()
            
            if not user_with_username:
                messages.error(request, "Username does not exist.")
            else:
                messages.error(request, "Wrong password")
            return redirect('loginAcc')


# this is for the contact form
def submit_contact_form(request):
    if request.method == 'POST':
 
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        message = request.POST.get('message')


        contact_model_instance = Contact(
            first_name=first_name,
            email=email,
            message=message,
            submission_time=timezone.now()  # Set the submission time to the current time
        )
        contact_model_instance.save()

        subject = 'Feedback Submission from the User'
        message_body = f"Name: {first_name}\nEmail: {email}\nMessage: {message}"

        recipient_email = '202080469@psu.palawan.edu.ph'

        send_mail(subject, message_body, email, [recipient_email])
        messages.success(request, 'Form submitted successfully!')
        return redirect('home') 
    else:
        return render(request, 'index.html')


def submit_developer_contact_form(request):
    if request.method == 'POST':
   
        name_admin = request.POST.get('name')
        issue = request.POST.get('issue')
        message_content = request.POST.get('message') 
        email = request.POST.get('email')

        devdeloper_contact_model_instance = Contact_Developer(name_admin=name_admin, issue=issue, messages=message_content)
        devdeloper_contact_model_instance.save()

        subject = 'New Feedback Submission from the Admin'
        message_body = f"Name: {name_admin}\nIssue: {issue}\nMessage: {message_content}"

        recipient_email = '202080469@psu.palawan.edu.ph'

        send_mail(subject, message_body, email, [recipient_email])
        messages.success(request, 'Form submitted successfully!')
        return redirect('dashboard')  
    else:
        return render(request, 'user-admin/dashboard.html')

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
    

