from django.urls import path
from .views import officials_dashboard_screen_view, officials_table_screen_view, officials_addacc_screen_view, add_account_form, login_account_form, submit_developer_contact_form, user_logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/dashboard/', officials_dashboard_screen_view, name='dashboard'),
    path('login/table/', officials_table_screen_view, name='table'),
    path('login/AddAccount', officials_addacc_screen_view, name='AddAcc'),
    path('add_account_form/', add_account_form, name='add_account_form'),
    path('login_account_form/', login_account_form, name='login_account_form'),
    path('user_logout/', user_logout, name='user_logout'),
    path('submit_developer_contact_form/', submit_developer_contact_form, name='submit_developer_contact_form'),
    

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='admin-forgotpass.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'), name="password_reset_done"),
    path('reset_password_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='admin-changepass.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'), name="password_reset_complete"),

   
]

    # path('forgot_pass_form/', forgot_pass_screen_view, name='forgot-pass'),
    # path('forgotpass/', ForgetPassword, name='forgotpassword'),
    # path('change_pass/<str:token>/', change_pass_screen_view, name='change-pass'),