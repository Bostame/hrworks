from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    manage_users, delete_user, edit_user, clock_in, clock_out, dashboard, get_live_hours, export_pdf,
    telephone_directory, company_calendar, company_calendar_view, add_event
)

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('register/', views.register_user, name='register_user'), 
    path('my-profile/', views.my_profile, name='my_profile'),
    path('clock-in/', clock_in, name='clock_in'),
    path('clock-out/', clock_out, name='clock_out'),
    path('get_live_hours/', get_live_hours, name='get_live_hours'),
    path('export/pdf/', export_pdf, name='export_pdf'),

    # ✅ Company Overview URLs
    path('company-overview/telephone-directory/', views.telephone_directory, name='telephone_directory'),
    path('company-overview/company-information/', views.company_information, name='company_information'),
    path('company-overview/company-calendar/', company_calendar, name='company_calendar'),
    path('company-overview/company-calendar/add/', add_event, name='add_event'),
    path('company-overview/company-calendar/<str:view_type>/', company_calendar_view, name='company_calendar_view'),
    path('company-overview/company-calendar/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('company-overview/company-calendar/delete/<int:event_id>/', views.delete_event, name='delete_event'),

    # ✅ User Management
    path("manage-users/", manage_users, name="manage_users"),
    path("edit-user/<int:user_id>/", edit_user, name="edit_user"),
    path("delete-user/<int:user_id>/", delete_user, name="delete_user"),
    
]