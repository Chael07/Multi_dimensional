
from django.urls import path
from .views import officials_dashboard_screen_view, household_table_screen_view, profile_table_screen_view, officials_addacc_screen_view, add_account_form, login_account_form, submit_developer_contact_form, user_logout, archive, Admin_account_form, admin_logout, archive_table_screen_view 
from .views import return_data
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/dashboard/', officials_dashboard_screen_view, name='dashboard'),
    path('login/household/', household_table_screen_view, name='household_table'),
    path('login/household/profile/', profile_table_screen_view, name='household_profile_table'),
    path('login/household/archive/', archive_table_screen_view, name='archive_table_screen_view'),
    path('login/AddAccount', officials_addacc_screen_view, name='AddAcc'),
    path('add_account_form/', add_account_form, name='add_account_form'),
    path('login_account_form/', login_account_form, name='login_account_form'),
    path('admin_account_form/', Admin_account_form, name='Admin_account_form'),
    path('user_logout/', user_logout, name='user_logout'),
    path('admin_logout/', admin_logout, name='admin_logout'),
    path('submit_developer_contact_form/', submit_developer_contact_form, name='submit_developer_contact_form'),
    
    path('archive/<int:id>/', archive, name='archive'),
    path('return/<int:id>/', return_data, name='return'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='admin-forgotpass.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name="password_reset_done"),
    path('reset_password_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='admin-changepass.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name="password_reset_complete"),


]

    # path('forgot_pass_form/', forgot_pass_screen_view, name='forgot-pass'),
    # path('forgotpass/', ForgetPassword, name='forgotpassword'),
    # path('change_pass/<str:token>/', change_pass_screen_view, name='change-pass'),