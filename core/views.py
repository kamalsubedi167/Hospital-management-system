from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Patient, Doctor, Appointment, Medicine, LabReport, Billing, Diagnosis,Notification
from .forms import PatientForm, DoctorForm, AppointmentForm, MedicineForm, LabReportForm, BillingForm
from django.db.models import Q, Count
from django.utils import timezone
from datetime import date, timedelta
import json
from django.db.models.functions import TruncMonth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_doctor(user):
    return user.groups.filter(name='Doctor').exists()

def is_admin_or_doctor(user):
    return user.groups.filter(name='Admin').exists() or user.groups.filter(name='Doctor').exists()

def home(request):
    return render(request, 'home.html')

@login_required
@user_passes_test(is_admin_or_doctor)
def patient_list(request):
    if request.user.groups.filter(name='Doctor').exists():
        try:
            doctor = Doctor.objects.get(user=request.user)
            patients = Patient.objects.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            patients = Patient.objects.none()
    else:
        query = request.GET.get('q')
        if query:
            patients = Patient.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(patient_id__icontains=query)
            )
        else:
            patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})

@login_required
@user_passes_test(is_admin)
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'add_patient.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('patient_list')
    else:
        form = PatientForm(instance=patient)
    return render(request, 'edit_patient.html', {'form': form, 'patient': patient})

@login_required
@user_passes_test(is_admin)
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patient_list.html', {'patients': Patient.objects.all()})

@login_required
@user_passes_test(is_admin_or_doctor)
def dashboard(request):
    Notification.objects.filter(user=request.user).delete()
    if request.user.groups.filter(name='Doctor').exists():
        try:
            doctor = Doctor.objects.get(user=request.user)
            total_patients = Patient.objects.filter(doctor=doctor).count()
            total_doctors = 1  # Only the logged-in doctor
            today = date.today()
            todays_appointments = Appointment.objects.filter(
                doctor=doctor, appointment_date__date=today
            ).count()
            upcoming_appointments = Appointment.objects.filter(
                doctor=doctor, appointment_date__gte=timezone.now()
            ).order_by('appointment_date')[:5]
            pending_lab_reports = LabReport.objects.filter(
                patient__doctor=doctor, is_pending=True
            ).count()
            low_stock_medicines = 0  # Doctors don't have access to pharmacy
            unpaid_bills = 0  # Doctors don't have access to billing
            # Chart data for doctors
            registration_data = Patient.objects.filter(
                doctor=doctor,
                created_at__gte=timezone.now() - timedelta(days=180)
            ).annotate(
                month=TruncMonth('created_at')
            ).values('month').annotate(count=Count('id')).order_by('month')
            diseases_data = Diagnosis.objects.filter(
                patient__doctor=doctor
            ).values('disease').annotate(count=Count('id')).order_by('-count')[:5]

        # Notificationtest
            upcoming_appointments_notify = Appointment.objects.filter(
                doctor=doctor,
                appointment_date__gte=timezone.now(),
                appointment_date__lte=timezone.now() + timedelta(hours=24)
            )
            for appt in upcoming_appointments_notify:
                Notification.objects.create(
                    user=request.user,
                    message=f"Upcoming appointment with {appt.patient} at {appt.appointment_date}",
                )

                # Notificationtest
        except Doctor.DoesNotExist:
            total_patients = total_doctors = todays_appointments = pending_lab_reports = 0
            upcoming_appointments = []
            unpaid_bills = 0
            registration_data = []
            diseases_data = []
    else:
        total_patients = Patient.objects.count()
        total_doctors = Doctor.objects.count()
        today = date.today()
        todays_appointments = Appointment.objects.filter(
            appointment_date__date=today
        ).count()
        upcoming_appointments = Appointment.objects.filter(
            appointment_date__gte=timezone.now()
        ).order_by('appointment_date')[:5]
        pending_lab_reports = LabReport.objects.filter(is_pending=True).count()
        low_stock_medicines = Medicine.objects.filter(stock__lt=10).count()
        unpaid_bills = Billing.objects.filter(is_paid=False).count()
        # Chart data for admins
        registration_data = Patient.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=180)
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(count=Count('id')).order_by('month')
        diseases_data = Diagnosis.objects.values('disease').annotate(count=Count('id')).order_by('-count')[:5]

        # Notificationtest
        upcoming_appointments_notify = Appointment.objects.filter(
            appointment_date__gte=timezone.now(),
            appointment_date__lte=timezone.now() + timedelta(hours=24)
        )
        for appt in upcoming_appointments_notify:
            Notification.objects.create(
                user=request.user,
                message=f"Upcoming appointment: {appt.patient} with {appt.doctor} at {appt.appointment_date}",
            )

        unpaid_bills_notify = Billing.objects.filter(is_paid=False)
        for bill in unpaid_bills_notify:
            Notification.objects.create(
                user=request.user,
                message=f"Unpaid bill for {bill.patient}: ${bill.amount} due on {bill.bill_date}",
            )
        # Notificationtest

    # Prepare registration trend data for the past 6 months
    import calendar
    from datetime import datetime
    today = timezone.now().date()
    months = []
    counts = []
    for i in range(5, -1, -1):
        month_date = today - timedelta(days=30 * i)
        month_name = calendar.month_name[month_date.month][:3] + f" {month_date.year}"
        months.append(month_name)
        count = next((item['count'] for item in registration_data if item['month'].date().month == month_date.month and item['month'].date().year == month_date.year), 0)
        counts.append(count)

    # Prepare diseases data
    disease_labels = [item['disease'] for item in diseases_data]
    disease_counts = [item['count'] for item in diseases_data]
    # Notificationtest
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    # Notificationtest

    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'todays_appointments': todays_appointments,
        'upcoming_appointments': upcoming_appointments,
        'pending_lab_reports': pending_lab_reports,
        'low_stock_medicines': low_stock_medicines,
        'unpaid_bills': unpaid_bills,
        'registration_months': json.dumps(months),
        'registration_counts': json.dumps(counts),
        'disease_labels': json.dumps(disease_labels),
        'disease_counts': json.dumps(disease_counts),
         'notifications': notifications,
    }
    return render(request, 'dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})

@login_required
@user_passes_test(is_admin)
def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('doctor_list')
    else:
        form = DoctorForm()
    return render(request, 'add_doctor.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_doctor)
def doctor_profile(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    if request.user.groups.filter(name='Doctor').exists() and doctor.user != request.user:
        return redirect('dashboard')
    assigned_patients = Patient.objects.filter(doctor=doctor)
    context = {
        'doctor': doctor,
        'assigned_patients': assigned_patients,
    }
    return render(request, 'doctor_profile.html', context)

@login_required
@user_passes_test(is_admin_or_doctor)
def appointment_list(request):
    filter_by = request.GET.get('filter_by', 'all')
    if request.user.groups.filter(name='Doctor').exists():
        try:
            doctor = Doctor.objects.get(user=request.user)
            appointments = Appointment.objects.filter(
                doctor=doctor, appointment_date__gte=timezone.now()
            ).order_by('appointment_date')
        except Doctor.DoesNotExist:
            appointments = Appointment.objects.none()
    else:
        appointments = Appointment.objects.filter(
            appointment_date__gte=timezone.now()
        ).order_by('appointment_date')
        if filter_by == 'patient' and request.GET.get('patient_id'):
            appointments = appointments.filter(patient_id=request.GET.get('patient_id'))
        elif filter_by == 'doctor' and request.GET.get('doctor_id'):
            appointments = appointments.filter(doctor_id=request.GET.get('doctor_id'))
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    context = {
        'appointments': appointments,
        'patients': patients,
        'doctors': doctors,
        'filter_by': filter_by,
    }
    return render(request, 'appointment_list.html', context)

@login_required
@user_passes_test(is_admin)
def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'add_appointment.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def edit_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'edit_appointment.html', {'form': form, 'appointment': appointment})

@login_required
@user_passes_test(is_admin)
def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    return render(request, 'appointment_list.html', {'appointments': Appointment.objects.all()})

@login_required
@user_passes_test(is_admin)
def medicine_list(request):
    query = request.GET.get('q')
    if query:
        medicines = Medicine.objects.filter(
            Q(name__icontains=query) |
            Q(type__icontains=query)
        )
    else:
        medicines = Medicine.objects.all()
    return render(request, 'medicine_list.html', {'medicines': medicines})

@login_required
@user_passes_test(is_admin)
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm()
    return render(request, 'add_medicine.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_medicine_stock(request, id):
    medicine = get_object_or_404(Medicine, id=id)
    if request.method == 'POST':
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine_list')
    else:
        form = MedicineForm(instance=medicine)
    return render(request, 'update_medicine_stock.html', {'form': form, 'medicine': medicine})

@login_required
@user_passes_test(is_admin_or_doctor)
def lab_report_list(request):
    show_pending = request.GET.get('show_pending', 'all')
    if request.user.groups.filter(name='Doctor').exists():
        try:
            doctor = Doctor.objects.get(user=request.user)
            if show_pending == 'pending':
                lab_reports = LabReport.objects.filter(
                    patient__doctor=doctor, is_pending=True
                )
            else:
                lab_reports = LabReport.objects.filter(patient__doctor=doctor)
        except Doctor.DoesNotExist:
            lab_reports = LabReport.objects.none()
    else:
        if show_pending == 'pending':
            lab_reports = LabReport.objects.filter(is_pending=True)
        else:
            lab_reports = LabReport.objects.all()
    context = {
        'lab_reports': lab_reports,
        'show_pending': show_pending,
    }
    return render(request, 'lab_report_list.html', context)

@login_required
@user_passes_test(is_admin)
def add_lab_report(request):
    if request.method == 'POST':
        form = LabReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lab_report_list')
    else:
        form = LabReportForm()
    return render(request, 'add_lab_report.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_lab_report(request, id):
    lab_report = get_object_or_404(LabReport, id=id)
    if request.method == 'POST':
        form = LabReportForm(request.POST, instance=lab_report)
        if form.is_valid():
            form.save()
            return redirect('lab_report_list')
    else:
        form = LabReportForm(instance=lab_report)
    return render(request, 'update_lab_report.html', {'form': form, 'lab_report': lab_report})

@login_required
@user_passes_test(is_admin)
def billing_list(request):
    bills = Billing.objects.all()
    return render(request, 'billing_list.html', {'bills': bills})

@login_required
@user_passes_test(is_admin)
def add_billing(request):
    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('billing_list')
    else:
        form = BillingForm()
    return render(request, 'add_billing.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def update_billing(request, id):
    bill = get_object_or_404(Billing, id=id)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('billing_list')
    else:
        form = BillingForm(instance=bill)
    return render(request, 'update_billing.html', {'form': form, 'bill': bill})

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def profile(request):
    if request.method == 'POST':
        # Update user details (name, email)
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        # Handle password change
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Your password was updated successfully.")
        else:
            for error in password_form.errors.values():
                messages.error(request, error)

        messages.success(request, "Profile updated successfully.")
        return redirect('profile')

    else:
        password_form = PasswordChangeForm(request.user)

    context = {
        'password_form': password_form,
    }
    return render(request, 'profile.html', context)