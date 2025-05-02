from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Patient, Doctor, Appointment, Medicine, LabReport, Billing, Diagnosis, Notification
from .forms import PatientForm, DoctorForm, AppointmentForm, MedicineForm, LabReportForm, BillingForm
from django.db.models import Q, Count
from django.utils import timezone
from datetime import date, timedelta, datetime
import json
from django.db.models.functions import TruncMonth
from django.db import IntegrityError
from django.contrib import messages
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
        patients = Patient.objects.all()
        doctors = Doctor.objects.all()

        # Search by name or patient ID
        query = request.GET.get('q')
        if query:
            patients = patients.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(patient_id__icontains=query)
            )

        # Filter by doctor
        doctor_id = request.GET.get('doctor_id')
        if doctor_id:
            patients = patients.filter(doctor_id=doctor_id)

        # Filter by gender
        gender = request.GET.get('gender')
        if gender:
            patients = patients.filter(gender=gender)

        # Filter by blood group
        blood_group = request.GET.get('blood_group')
        if blood_group:
            patients = patients.filter(blood_group=blood_group)

        context = {
            'patients': patients,
            'doctors': doctors,
            'selected_doctor': doctor_id,
            'selected_gender': gender,
            'selected_blood_group': blood_group,
            'query': query,
        }
        return render(request, 'patient_list.html', context)

    return render(request, 'patient_list.html', {'patients': patients})

@login_required
@user_passes_test(is_admin)
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Patient added successfully.")
                return redirect('patient_list')
            except IntegrityError:
                messages.error(request, "A patient with this ID already exists. Please use a unique Patient ID.")
        else:
            messages.error(request, "Please correct the errors in the form.")
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
            try:
                form.save()
                messages.success(request, "Patient updated successfully.")
                return redirect('patient_list')
            except IntegrityError:
                messages.error(request, "A patient with this ID already exists. Please use a unique Patient ID.")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = PatientForm(instance=patient)
    return render(request, 'edit_patient.html', {'form': form, 'patient': patient})

@login_required
@user_passes_test(is_admin)
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        patient.delete()
        messages.success(request, "Patient deleted successfully.")
        return redirect('patient_list')
    return render(request, 'patient_list.html', {'patients': Patient.objects.all()})

@login_required
@user_passes_test(is_admin_or_doctor)
def dashboard(request):
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

            # Notifications for upcoming appointments
            upcoming_appointments_notify = Appointment.objects.filter(
                doctor=doctor,
                appointment_date__gte=timezone.now(),
                appointment_date__lte=timezone.now() + timedelta(hours=24)
            )
            for appt in upcoming_appointments_notify:
                # Check if a notification for this appointment already exists
                message = f"Upcoming appointment with {appt.patient} at {appt.appointment_date}"
                if not Notification.objects.filter(user=request.user, message=message).exists():
                    Notification.objects.create(
                        user=request.user,
                        message=message,
                    )

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

        # Notifications for admins
        upcoming_appointments_notify = Appointment.objects.filter(
            appointment_date__gte=timezone.now(),
            appointment_date__lte=timezone.now() + timedelta(hours=24)
        )
        for appt in upcoming_appointments_notify:
            message = f"Upcoming appointment: {appt.patient} with {appt.doctor} at {appt.appointment_date}"
            if not Notification.objects.filter(user=request.user, message=message).exists():
                Notification.objects.create(
                    user=request.user,
                    message=message,
                )

        unpaid_bills_notify = Billing.objects.filter(is_paid=False)
        for bill in unpaid_bills_notify:
            message = f"Unpaid bill for {bill.patient}: ${bill.amount} due on {bill.bill_date}"
            if not Notification.objects.filter(user=request.user, message=message).exists():
                Notification.objects.create(
                    user=request.user,
                    message=message,
                )

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

    # Fetch notifications
    notifications = Notification.objects.filter(user=request.user, is_read=False)

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
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status = request.GET.get('status', 'upcoming')

    if request.user.groups.filter(name='Doctor').exists():
        try:
            doctor = Doctor.objects.get(user=request.user)
            appointments = Appointment.objects.filter(doctor=doctor)
        except Doctor.DoesNotExist:
            appointments = Appointment.objects.none()
    else:
        appointments = Appointment.objects.all()
        patients = Patient.objects.all()
        doctors = Doctor.objects.all()

    # Filter by status (upcoming or past)
    if status == 'upcoming':
        appointments = appointments.filter(appointment_date__gte=timezone.now())
    elif status == 'past':
        appointments = appointments.filter(appointment_date__lt=timezone.now())

    # Filter by date range
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            appointments = appointments.filter(appointment_date__date__gte=start_date)
        except ValueError:
            messages.error(request, "Invalid start date format. Use YYYY-MM-DD.")
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            appointments = appointments.filter(appointment_date__date__lte=end_date)
        except ValueError:
            messages.error(request, "Invalid end date format. Use YYYY-MM-DD.")

    # Existing filters (patient or doctor)
    if filter_by == 'patient' and request.GET.get('patient_id'):
        appointments = appointments.filter(patient_id=request.GET.get('patient_id'))
    elif filter_by == 'doctor' and request.GET.get('doctor_id'):
        appointments = appointments.filter(doctor_id=request.GET.get('doctor_id'))

    appointments = appointments.order_by('appointment_date')

    if request.user.groups.filter(name='Doctor').exists():
        context = {
            'appointments': appointments,
            'filter_by': filter_by,
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
        }
    else:
        context = {
            'appointments': appointments,
            'patients': patients,
            'doctors': doctors,
            'filter_by': filter_by,
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
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
    test_name = request.GET.get('test_name')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if request.user.groups.filter(name='Doctor').exists():
        try:
            doctor = Doctor.objects.get(user=request.user)
            lab_reports = LabReport.objects.filter(patient__doctor=doctor)
        except Doctor.DoesNotExist:
            lab_reports = LabReport.objects.none()
    else:
        lab_reports = LabReport.objects.all()

    # Filter by pending status
    if show_pending == 'pending':
        lab_reports = lab_reports.filter(is_pending=True)

    # Filter by test name
    if test_name:
        lab_reports = lab_reports.filter(test_name__icontains=test_name)

    # Filter by date range
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            lab_reports = lab_reports.filter(date__gte=start_date)
        except ValueError:
            messages.error(request, "Invalid start date format. Use YYYY-MM-DD.")
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            lab_reports = lab_reports.filter(date__lte=end_date)
        except ValueError:
            messages.error(request, "Invalid end date format. Use YYYY-MM-DD.")

    context = {
        'lab_reports': lab_reports,
        'show_pending': show_pending,
        'test_name': test_name,
        'start_date': start_date,
        'end_date': end_date,
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

@login_required
@user_passes_test(is_admin_or_doctor)
def patient_profile(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.user.groups.filter(name='Doctor').exists():
        try:
            doctor = Doctor.objects.get(user=request.user)
            if patient.doctor != doctor:
                messages.error(request, "You do not have permission to view this patient's profile.")
                return redirect('patient_list')
        except Doctor.DoesNotExist:
            messages.error(request, "Doctor profile not found.")
            return redirect('patient_list')

    appointments = Appointment.objects.filter(patient=patient).order_by('-appointment_date')
    diagnoses = Diagnosis.objects.filter(patient=patient).order_by('-diagnosis_date')
    lab_reports = LabReport.objects.filter(patient=patient).order_by('-date')

    context = {
        'patient': patient,
        'appointments': appointments,
        'diagnoses': diagnoses,
        'lab_reports': lab_reports,
    }
    return render(request, 'patient_profile.html', context)

@login_required
def mark_notification_read(request, id):
    notification = get_object_or_404(Notification, id=id, user=request.user)
    print(f"Before update: Notification {notification.id}, is_read = {notification.is_read}")
    notification.is_read = True
    notification.save()
    print(f"After update: Notification {notification.id}, is_read = {notification.is_read}")
    messages.success(request, "Notification marked as read.")
    return redirect('dashboard')