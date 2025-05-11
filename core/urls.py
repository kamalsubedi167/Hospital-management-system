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
    path('pharmacy/', views.medicine_list, name='medicine_list'),
    path('pharmacy/add/', views.add_medicine, name='add_medicine'),
    path('pharmacy/update/<int:id>/', views.update_medicine_stock, name='update_medicine_stock'),
    path('lab-reports/', views.lab_report_list, name='lab_report_list'),
    path('lab-reports/add/', views.add_lab_report, name='add_lab_report'),
    path('lab-reports/update/<int:id>/', views.update_lab_report, name='update_lab_report'),
    path('billing/', views.billing_list, name='billing_list'),
    path('billing/add/', views.add_billing, name='add_billing'),
    path('billing/update/<int:id>/', views.update_billing, name='update_billing'),
    path('profile/', views.profile, name='profile'),
    path('patient/<int:id>/', views.patient_profile, name='patient_profile'),
    path('notification/<int:id>/mark_read/', views.mark_notification_read, name='mark_notification_read'),
    path('appointments/export/', views.export_appointments_csv, name='export_appointments_csv'),
    path('patients/export/', views.export_patients_csv, name='export_patients_csv'),
    path('feedback/', views.feedback_list, name='feedback_list'),
    path('feedback/submit/', views.submit_feedback, name='submit_feedback'),
    path('feedback/resolve/<int:id>/', views.resolve_feedback, name='resolve_feedback'),
    path('patients/<int:id>/report/', views.generate_patient_report, name='generate_patient_report'),
    path('audit-logs/', views.audit_log_list, name='audit_log_list'),

]

