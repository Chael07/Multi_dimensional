from django.urls import path
from .views import officials_dashboard_screen_view, officials_table_screen_view, officials_addacc_screen_view, add_account_form, login_account_form, forgot_pass_screen_view, change_pass_screen_view,ChangePassword
#   

urlpatterns = [
    path('login/dashboard/', officials_dashboard_screen_view, name='dashboard'),
    path('login/table/', officials_table_screen_view, name='table'),
    path('login/AddAccount', officials_addacc_screen_view, name='AddAcc'),
    path('add_account_form/', add_account_form, name='add_account_form'),
    path('login_account_form/', login_account_form, name='login_account_form'),

    path('forgot_pass_form/', forgot_pass_screen_view, name='forgot-pass'),
    path('forgotpass/', ChangePassword, name='changepassword'),
    path('change_pass_form/', change_pass_screen_view, name='change-pass'),
    

]

# path('reset_password/', auth_views.PasswordResetView.as_view(), name="reset_password"),
#     path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
#     path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
#     path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),