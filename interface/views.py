
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
import pandas as pd


from .models import Household
from .models import Contact
from .models import Contact_Developer
from .models import HouseholdProfile , result_classify, ResultMPI
from .models import Backup_Household, Backup_HouseholdProfile, Backup_ResultMPI, Backup_result_classify

import joblib
from django.conf import settings

def home_screen_view(request):
	print(request.headers)
	return render(request, "index.html", {})

def user_login_view(request):
    print(request.headers)
    return render(request, "user-login.html", {})

def privacy_screen_view(request):
	print(request.headers)
	return render(request, "privacy.html", {})

def evaluation_screen_view(request):
	print(request.headers)
	return render(request, "eval.html", {})

def login_acc(request):
	print(request.headers)
	return render(request, "admin-login.html", {})

def user_logout(request):
    logout(request)
    return redirect('userlogin')

def admin_logout(request):
    logout(request)
    return redirect('loginAcc')


def officials_dashboard_screen_view(request):
    print(request.headers)
    contact_data_set = Contact.objects.all().order_by('-submission_time')[:5]
    poor_count_svm, non_poor_count_svm = get_poor_non_poor_counts()

    # Assuming you have a queryset for Household and household_profile models
    household_data = Household.objects.values('indi1', 'indi3', 'indi4', 'indi5', 'indi6', 'indi7', 'indi8', 'indi9',  'indi11', 'indi12')
    profile_data = ResultMPI.objects.values('mpi')

    # Convert queryset to DataFrame
    household_df = pd.DataFrame.from_records(household_data)
    profile_df = pd.DataFrame.from_records(profile_data)

    # Concatenate DataFrames along columns
    data = pd.concat([household_df, profile_df], axis=1)
    
    indicator_mapping = {
    'indi1': 'Educational Attainment',
    'indi3': 'Hunger',
    'indi4': 'Food Consumption',
    'indi5': 'Health Insurance',
    'indi6': 'Ownership of Assets',
    'indi7': 'Toilet Facility',
    'indi8': 'Access to Water',
    'indi9': 'Access to Electricity',
    'indi11': 'Housing Material',
    'indi12': 'Underemployment',
    }
 
    # Calculate the correlation matrix
    correlation_matrix = data.corr()

    # Identify the top 5 indicators based on correlation with the target variable
    target_variable = 'mpi' 
    top_indicators = correlation_matrix[target_variable].abs().sort_values(ascending=False).index[1:6]
    top_indicator_scores = correlation_matrix.loc[top_indicators, target_variable].values

    print("Top 5 indicators based on correlation with '{}':".format(target_variable))
    for indicator, score in zip(top_indicators, top_indicator_scores):
        display_name = indicator_mapping.get(indicator, indicator)
        print(f"{display_name}: {score:.4f}")

    display_data = [{'name': indicator_mapping.get(indicator, indicator), 'score': score} for indicator, score in zip(top_indicators, top_indicator_scores)]
    context = {
        'top_indicators': display_data,
        'contact_data_set': contact_data_set, 
        'poor_count_svm': poor_count_svm,
        'non_poor_count_svm': non_poor_count_svm,
    }

    return render(request, "user-admin/dashboard.html", context)


def get_poor_non_poor_counts():
    # Fetch data from the Household model
    result_classify_data = result_classify.objects.values('svm_result')
    # Initialize counters
    # poor_count_dt = 0
    # non_poor_count_dt = 0
    poor_count_svm = 0
    non_poor_count_svm = 0

    # Count based on the values of q1, q2, q3, and q4
    # for record in result_classify_data:
    #     if record['dt_result'] == 0.0:
    #         poor_count_dt += 1
    #     else:
    #         non_poor_count_dt += 1
    for record in result_classify_data:
        if record['svm_result'] == 0.0:
            poor_count_svm += 1
        else:
            non_poor_count_svm += 1

        
    return poor_count_svm, non_poor_count_svm


def map_to_poor_non_poor(value):
    # Map 1 to "Non-poor" and 0 to "Poor"
    if value == 1:
        return "Non-poor"
    elif value == 0:
        return "Poor"
    else:
        return "None"

def archive_table_screen_view(request):
    print(request.headers)

    result_mpi_data = Backup_ResultMPI.objects.values('id', 'mpi')
    result_classify_data = Backup_result_classify.objects.values('id', 'svm_result')
    household_profile_data = Backup_HouseholdProfile.objects.values('id', 'relationship', 'user_number', 'user_email', 'user_address')

    combined_data = []

    for profile_row in household_profile_data:
        profile_id = profile_row['id']

        # Find the matching row in result_mpi_data
        mpi_row = next((row for row in result_mpi_data if row['id'] == profile_id), None)

        # Find the matching row in result_classify_data
        classify_row = next((row for row in result_classify_data if row['id'] == profile_id), None)

        if mpi_row:
            # Combine the data from both tables
            combined_row = {**profile_row, **mpi_row}

            # Add svm_result to the combined data if available
            if classify_row:
                combined_row['svm_result'] = map_to_poor_non_poor(classify_row['svm_result'])

            combined_data.append(combined_row)

    # Order the combined data by the 'id' field
    combined_data = sorted(combined_data, key=lambda x: x['id'])
    paginator = Paginator(combined_data, 30)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj
    }

    return render(request, "user-admin/archive_data.html", context)

def profile_table_screen_view(request):
    print(request.headers)

    result_mpi_data = ResultMPI.objects.values('id', 'mpi')
    result_classify_data = result_classify.objects.values('id', 'svm_result')
    household_profile_data = HouseholdProfile.objects.values('id', 'relationship', 'user_number', 'user_email', 'user_address')

    combined_data = []

    for profile_row in household_profile_data:
        profile_id = profile_row['id']

        # Find the matching row in result_mpi_data
        mpi_row = next((row for row in result_mpi_data if row['id'] == profile_id), None)

        # Find the matching row in result_classify_data
        classify_row = next((row for row in result_classify_data if row['id'] == profile_id), None)

        if mpi_row:
            # Combine the data from both tables
            combined_row = {**profile_row, **mpi_row}

            # Add svm_result to the combined data if available
            if classify_row:
                combined_row['svm_result'] = map_to_poor_non_poor(classify_row['svm_result'])

            combined_data.append(combined_row)

    # Order the combined data by the 'id' field
    combined_data = sorted(combined_data, key=lambda x: x['id'])
    paginator = Paginator(combined_data, 30)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj
    }

    return render(request, "user-admin/profile_table.html", context)



def archive(request, id):
    # Get the household_profile instance by ID
    household_profile_instance = HouseholdProfile.objects.get(id=id)

        # Create backup instances before deletion
    backup_household_profile = Backup_HouseholdProfile(
        id=household_profile_instance.id,
        relationship=household_profile_instance.relationship,
        user_number=household_profile_instance.user_number,
        user_address=household_profile_instance.user_address,
        user_email=household_profile_instance.user_email
    )
    backup_household_profile.save()

    # Get corresponding Household instance and create backup
    household_instance = Household.objects.get(id=id)
    backup_household = Backup_Household(
        id=household_instance.id,
        indi1=household_instance.indi1,
        indi2=household_instance.indi2,
        indi3=household_instance.indi3,
        indi4=household_instance.indi4,
        indi5=household_instance.indi5,
        indi6=household_instance.indi6,
        indi7=household_instance.indi7,
        indi8=household_instance.indi8,
        indi9=household_instance.indi9,
        indi10=household_instance.indi10,
        indi11=household_instance.indi11,
        indi12=household_instance.indi12,
        indi13=household_instance.indi13,
    )
    backup_household.save()

    # Get corresponding ResultClassify instance and create backup
    result_classify_instance = result_classify.objects.get(id=id)
    backup_result_classify = Backup_result_classify(
        id=result_classify_instance.id,
        svm_result=result_classify_instance.svm_result
    )
    backup_result_classify.save()

    # Get corresponding ResultMPI instance and create backup
    result_mpi_instance = ResultMPI.objects.get(id=id)
    backup_result_mpi = Backup_ResultMPI(
        id=result_mpi_instance.id,
        mpi=result_mpi_instance.mpi
    )
    backup_result_mpi.save()

    # Get corresponding Household and result_classify instances
    household_instance = Household.objects.get(id=id)
    result_classify_instance = result_classify.objects.get(id=id)
    result_mpi_instance = ResultMPI.objects.get(id=id)

    # Delete instances from all three tables
    household_profile_instance.delete()
    household_instance.delete()
    result_classify_instance.delete()
    result_mpi_instance.delete()

    return redirect('household_profile_table')

def return_data(request, id):
    # Get the household_profile instance by ID
    household_profile_instance = Backup_HouseholdProfile.objects.get(id=id)

        # Create backup instances before deletion
    backup_household_profile = HouseholdProfile(
        id=household_profile_instance.id,
        relationship=household_profile_instance.relationship,
        user_number=household_profile_instance.user_number,
        user_address=household_profile_instance.user_address,
        user_email=household_profile_instance.user_email
    )
    backup_household_profile.save()

    # Get corresponding Household instance and create backup
    household_instance = Backup_Household.objects.get(id=id)
    backup_household = Household(
        id=household_instance.id,
        indi1=household_instance.indi1,
        indi2=household_instance.indi2,
        indi3=household_instance.indi3,
        indi4=household_instance.indi4,
        indi5=household_instance.indi5,
        indi6=household_instance.indi6,
        indi7=household_instance.indi7,
        indi8=household_instance.indi8,
        indi9=household_instance.indi9,
        indi10=household_instance.indi10,
        indi11=household_instance.indi11,
        indi12=household_instance.indi12,
        indi13=household_instance.indi13,
    )
    backup_household.save()

    # Get corresponding ResultClassify instance and create backup
    result_classify_instance = Backup_result_classify.objects.get(id=id)
    backup_result_classify = result_classify(
        id=result_classify_instance.id,
        svm_result=result_classify_instance.svm_result
    )
    backup_result_classify.save()

    # Get corresponding ResultMPI instance and create backup
    result_mpi_instance = Backup_ResultMPI.objects.get(id=id)
    backup_result_mpi = ResultMPI(
        id=result_mpi_instance.id,
        mpi=result_mpi_instance.mpi
    )
    backup_result_mpi.save()

    # Get corresponding Household and result_classify instances
    household_instance = Backup_Household.objects.get(id=id)
    result_classify_instance = Backup_result_classify.objects.get(id=id)
    result_mpi_instance = Backup_ResultMPI.objects.get(id=id)

    # Delete instances from all three tables
    household_profile_instance.delete()
    household_instance.delete()
    result_classify_instance.delete()
    result_mpi_instance.delete()

    return redirect('archive_table_screen_view')



def household_table_screen_view(request):
    print(request.headers)
    indi1_no, indi1_yes = get_indi1_counts()
    indi2_no, indi2_yes = get_indi2_counts()
    indi3_no, indi3_yes = get_indi3_counts()
    indi4_no, indi4_yes = get_indi4_counts()
    indi5_no, indi5_yes = get_indi5_counts()
    indi6_no, indi6_yes = get_indi6_counts()
    indi7_no, indi7_yes = get_indi7_counts()
    indi8_no, indi8_yes = get_indi8_counts()
    indi9_no, indi9_yes = get_indi9_counts()
    indi10_no, indi10_yes = get_indi10_counts()
    indi11_no, indi11_yes = get_indi11_counts()
    indi12_no, indi12_yes = get_indi12_counts()
    indi13_no, indi13_yes = get_indi13_counts()

    household_data = Household.objects.values('indi1', 'indi2', 'indi3', 'indi4', 'indi5', 'indi6', 'indi7', 'indi8', 'indi9', 'indi10', 'indi11', 'indi12', 'indi13').order_by('id')
    
    converted_household_data = []
    for record in household_data:
        converted_record = {key: convert_to_yes_no(value) for key, value in record.items()}
        converted_household_data.append(converted_record)
    print(converted_household_data)
    paginator = Paginator(converted_household_data, 30)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
        'indi1_no': indi1_no,
        'indi1_yes': indi1_yes, 
        'indi2_no': indi2_no,
        'indi2_yes': indi2_yes,
        'indi3_no': indi3_no,
        'indi3_yes': indi3_yes,
        'indi4_no': indi4_no,
        'indi4_yes': indi4_yes,
        'indi5_no': indi5_no,
        'indi5_yes': indi5_yes, 
        'indi6_no': indi6_no,
        'indi6_yes': indi6_yes,
        'indi7_no': indi7_no,
        'indi7_yes': indi7_yes,
        'indi8_no': indi8_no,
        'indi8_yes': indi8_yes,
        'indi9_no': indi9_no,
        'indi9_yes': indi9_yes, 
        'indi10_no': indi10_no,
        'indi10_yes': indi10_yes,
        'indi11_no': indi11_no,
        'indi11_yes': indi11_yes,
        'indi12_no': indi12_no,
        'indi12_yes': indi12_yes,
        'indi13_no': indi13_no,
        'indi13_yes': indi13_yes,
    }

    return render(request, "user-admin\Household_table.html", context)

def get_indi1_counts():
    household_data = Household.objects.values('indi1')
    indi1_no = 0
    indi1_yes = 0

    for record in household_data:
        if record['indi1'] == 0.0:
            indi1_no += 1
        else:
            indi1_yes += 1

    return indi1_no, indi1_yes

def get_indi2_counts():
    household_data = Household.objects.values('indi2')
    indi2_no = 0
    indi2_yes = 0

    for record in household_data:
        if record['indi2'] == 0.0:
            indi2_no += 1
        else:
            indi2_yes += 1

    return indi2_no, indi2_yes

def get_indi3_counts():
    household_data = Household.objects.values('indi3')
    indi3_no = 0
    indi3_yes = 0

    for record in household_data:
        if record['indi3'] == 0.0:
            indi3_no += 1
        else:
            indi3_yes += 1

    return indi3_no, indi3_yes

def get_indi4_counts():
    household_data = Household.objects.values('indi4')
    indi4_no = 0
    indi4_yes = 0

    for record in household_data:
        if record['indi4'] == 0.0:
            indi4_no += 1
        else:
            indi4_yes += 1

    return indi4_no, indi4_yes

def get_indi5_counts():
    household_data = Household.objects.values('indi5')
    indi5_no = 0
    indi5_yes = 0

    for record in household_data:
        if record['indi5'] == 0.0:
            indi5_no += 1
        else:
            indi5_yes += 1

    return indi5_no, indi5_yes

def get_indi6_counts():
    household_data = Household.objects.values('indi6')
    indi6_no = 0
    indi6_yes = 0

    for record in household_data:
        if record['indi6'] == 0.0:
            indi6_no += 1
        else:
            indi6_yes += 1

    return indi6_no, indi6_yes

def get_indi7_counts():
    household_data = Household.objects.values('indi7')
    indi7_no = 0
    indi7_yes = 0

    for record in household_data:
        if record['indi7'] == 0.0:
            indi7_no += 1
        else:
            indi7_yes += 1

    return indi7_no, indi7_yes

def get_indi8_counts():
    household_data = Household.objects.values('indi8')
    indi8_no = 0
    indi8_yes = 0

    for record in household_data:
        if record['indi8'] == 0.0:
            indi8_no += 1
        else:
            indi8_yes += 1

    return indi8_no, indi8_yes

def get_indi9_counts():
    household_data = Household.objects.values('indi9')
    indi9_no = 0
    indi9_yes = 0

    for record in household_data:
        if record['indi9'] == 0.0:
            indi9_no += 1
        else:
            indi9_yes += 1

    return indi9_no, indi9_yes

def get_indi10_counts():
    household_data = Household.objects.values('indi10')
    indi10_no = 0
    indi10_yes = 0

    for record in household_data:
        if record['indi10'] == 0.0:
            indi10_no += 1
        else:
            indi10_yes += 1

    return indi10_no, indi10_yes

def get_indi11_counts():
    household_data = Household.objects.values('indi11')
    indi11_no = 0
    indi11_yes = 0

    for record in household_data:
        if record['indi11'] == 0.0:
            indi11_no += 1
        else:
            indi11_yes += 1

    return indi11_no, indi11_yes

def get_indi12_counts():
    household_data = Household.objects.values('indi12')
    indi12_no = 0
    indi12_yes = 0

    for record in household_data:
        if record['indi12'] == 0.0:
            indi12_no += 1
        else:
            indi12_yes += 1

    return indi12_no, indi12_yes

def get_indi13_counts():
    household_data = Household.objects.values('indi13')
    indi13_no = 0
    indi13_yes = 0

    for record in household_data:
        if record['indi13'] == 0.0:
            indi13_no += 1
        else:
            indi13_yes += 1

    return indi13_no, indi13_yes

def convert_to_yes_no(value):
    if value == 0.076923077:
        return 'Deprived'
    elif value == 0.0:
        return 'Not-Deprived'
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

        # Check if the provided admin username already exists in the database
        if User.objects.filter(username=AdminUsername).exists():
            messages.error(request, f"The username '{AdminUsername}' is already taken. Please choose a different username.")
            return redirect('AddAcc')

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

    
def Admin_account_form(request):
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


def login_account_form(request):
    if request.method == 'POST':
        loginUsername = request.POST['Username']
        password1 = request.POST['password1']

        user = authenticate(username=loginUsername, password=password1)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Check if the username exists in the database
            user_with_username = User.objects.filter(username=loginUsername).exists()
            
            if not user_with_username:
                messages.error(request, "Username does not exist.")
            else:
                messages.error(request, "Wrong password")
            return redirect('userlogin')

# this is for the contact form

# def submit_contact_form(request):
#     if request.method == 'POST':
 
#         first_name = request.POST.get('first_name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')


#         contact_model_instance = Contact(
#             first_name=first_name,
#             email=email,
#             message=message,
#             submission_time=timezone.now()  
#         )
#         contact_model_instance.save()

#         subject = 'Feedback Submission from the User'
#         message_body = f"Name: {first_name}\nEmail: {email}\nMessage: {message}"

#         recipient_email = '202080469@psu.palawan.edu.ph'

#         send_mail(subject, message_body, email, [recipient_email])
#         messages.success(request, 'Form submitted successfully!')
#         return redirect('home') 
#     else:
#         return render(request, 'index.html')


def submit_developer_contact_form(request):
    if request.method == 'POST':
   
        name_admin = request.POST.get('name')
        issue = request.POST.get('issue')
        message_content = request.POST.get('message') 
        email = request.POST.get('email')

        devdeloper_contact_model_instance = Contact_Developer(name_admin=name_admin, issue=issue, messages=message_content)
        devdeloper_contact_model_instance.save()

        subject = 'New Feedback Submission from the Admin'
        message_body = f"Name: {name_admin}\nPosition: {issue}\nMessage: {message_content}"

        recipient_email = '202080469@psu.palawan.edu.ph'

        send_mail(subject, message_body, email, [recipient_email])
        messages.success(request, 'Form submitted successfully!')
        return redirect('dashboard')  
    else:
        return render(request, 'user-admin/dashboard.html')

# views.py

def submit_household(request):
    if request.method == 'POST':
        relationship = request.POST.get('relationship')
        user_email = request.POST.get('email')
        user_number = request.POST.get('Cnumber')
        user_address = request.POST.get('Address')

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

       
        
        return redirect(reverse('result') +
                    f'?relationship={relationship}&user_email={user_email}&user_number={user_number}&user_address={user_address}&q1={q1}&q2={q2}&q3={q3}&q4={q4}&q5={q5}&q6={q6}&q7={q7}&q8={q8}&q9={q9}&q10={q10}&q11={q11}&q12={q12}&q13={q13}')

    else:
        return render(request, 'eval.html')

def convert_to_one_zero(record):
    if record == 0.076923077:
        return '1'
    elif record == 0.0:
        return '0'
    else:
        return 'none'


def result_screen_view(request):
    print(request.headers)
    
    if request.method == 'GET':
        relationship = request.GET.get('relationship')
        user_email = request.GET.get('user_email')
        user_number = request.GET.get('user_number')
        user_address = request.GET.get('user_address')
        
        indi1 = float(request.GET.get('q1', 0))
        indi2 = float(request.GET.get('q2', 0))
        indi3 = float(request.GET.get('q3', 0))
        indi4 = float(request.GET.get('q4', 0))
        indi5 = float(request.GET.get('q5', 0))
        indi6 = float(request.GET.get('q6', 0))
        indi7 = float(request.GET.get('q7', 0))
        indi8 = float(request.GET.get('q8', 0))
        indi9 = float(request.GET.get('q9', 0))
        indi10 = float(request.GET.get('q10', 0))
        indi11 = float(request.GET.get('q11', 0))
        indi12 = float(request.GET.get('q12', 0))
        indi13 = float(request.GET.get('q13', 0))

        questions = [indi1, indi2, indi3, indi4, indi5, indi6, indi7, indi8, indi9, indi10, indi11, indi12, indi13]

        # Add both the "Deprived"/"Not Deprived" categories
        converted_questions = []
        for record in questions:
            converted_value = convert_to_one_zero(record)
            converted_questions.append(converted_value)
            
        count_yes = 0
        count_no = 0

        for response in questions:
            converted_value = convert_to_one_zero(response)

            if converted_value == '1':
                count_yes += 1
            elif converted_value == '0':
                count_no += 1

        clf_path = os.path.join(settings.BASE_DIR, 'interface/svm_model.joblib')
        clf = joblib.load(clf_path)
        result_data = [converted_questions] 
        prediction = clf.predict(result_data)

        prediction1 = '1' if prediction == 'Not Poor' else '0'

        result_classify.objects.create(svm_result= prediction1)
        household = Household.objects.create(
            indi1=indi1, indi2=indi2, indi3=indi3, indi4=indi4, indi5=indi5, indi6=indi6,
            indi7=indi7, indi8=indi8, indi9=indi9, indi10=indi10, indi11=indi11, indi12=indi12, indi13=indi13,
        )

        HouseholdProfile.objects.create(
            relationship = relationship,
            user_number = user_number,
            user_email=user_email,
            user_address = user_address,
        )

        question_mlr = [indi1, indi3, indi4, indi5, indi6, indi7, indi8, indi9, indi11, indi12,]

        mlf_path = os.path.join(settings.BASE_DIR, 'interface/mlr_model.joblib')
        mlf = joblib.load(mlf_path)
        result_data = [question_mlr]
        mlr_prediction = mlf.predict(result_data)

        ResultMPI.objects.create(mpi=mlr_prediction)

        prediction2 = 'Not Poor' if prediction == 'Not Poor' else 'Poor'
        context = {
            'prediction': prediction2,
            'count_yes': count_yes,
            'count_no': count_no
        }

        return render(request, "result.html", context)

