from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import clock_in, clock_out, dashboard, get_live_hours, export_pdf

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('register/', views.register_user, name='register_user'), 
    path('my-profile/', views.my_profile, name='my_profile'),
    path('clock-in/', clock_in, name='clock_in'),
    path('clock-out/', clock_out, name='clock_out'),
    path('get_live_hours/', get_live_hours, name='get_live_hours'),  # New API endpoint
    path('export/pdf/', export_pdf, name='export_pdf'),



]
