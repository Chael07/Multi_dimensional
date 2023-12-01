from django.urls import path
from .views import officials_dashboard_screen_view, officials_table_screen_view

app_name = 'officials'

urlpatterns = [
    path('login/dashboard/', officials_dashboard_screen_view, name='dashboard'),
    path('login/table/', officials_table_screen_view, name='table'),
]