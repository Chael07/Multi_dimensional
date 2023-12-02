from django.urls import path
from .views import officials_dashboard_screen_view, officials_table_screen_view, officials_addacc_screen_view, add_account_form, login_account_form


urlpatterns = [
    path('login/dashboard/', officials_dashboard_screen_view, name='dashboard'),
    path('login/table/', officials_table_screen_view, name='table'),
    path('login/AddAccount', officials_addacc_screen_view, name='AddAcc'),
    path('add_account_form/', add_account_form, name='add_account_form'),
    path('login_account_form/', login_account_form, name='login_account_form'),
]