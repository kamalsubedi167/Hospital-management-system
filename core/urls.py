from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.add_patient, name='add_patient'),
    path('patients/edit/<int:id>/', views.edit_patient, name='edit_patient'),
    path('patients/delete/<int:id>/', views.delete_patient, name='delete_patient'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/<int:id>/', views.doctor_profile, name='doctor_profile'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/add/', views.add_appointment, name='add_appointment'),
    path('appointments/edit/<int:id>/', views.edit_appointment, name='edit_appointment'),
    path('appointments/delete/<int:id>/', views.delete_appointment, name='delete_appointment'),
]
