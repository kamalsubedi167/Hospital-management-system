from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, Appointment, Medicine, LabReport
from .forms import PatientForm, DoctorForm, AppointmentForm, MedicineForm, LabReportForm
from django.db.models import Q, Count
from django.utils import timezone
from datetime import date

def home(request):
    return render(request, 'home.html')

@login_required
def patient_list(request):
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
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')
    return render(request, 'patient_list.html', {'patients': Patient.objects.all()})

@login_required
def dashboard(request):
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
    blood_group_counts = Patient.objects.values('blood_group').annotate(count=Count('blood_group')).order_by('blood_group')
    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'todays_appointments': todays_appointments,
        'upcoming_appointments': upcoming_appointments,
        'pending_lab_reports': pending_lab_reports,
        'low_stock_medicines': low_stock_medicines,
        'blood_group_counts': blood_group_counts,
    }
    return render(request, 'dashboard.html', context)

@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})

@login_required
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
def doctor_profile(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    assigned_patients = Patient.objects.filter(doctor=doctor)
    context = {
        'doctor': doctor,
        'assigned_patients': assigned_patients,
    }
    return render(request, 'doctor_profile.html', context)

@login_required
def appointment_list(request):
    filter_by = request.GET.get('filter_by', 'all')
    appointments = Appointment.objects.filter(appointment_date__gte=timezone.now()).order_by('appointment_date')
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
def delete_appointment(request, id):
    appointment = get_object_or_404(Appointment, id=id)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointment_list')
    return render(request, 'appointment_list.html', {'appointments': Appointment.objects.all()})

@login_required
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
def lab_report_list(request):
    show_pending = request.GET.get('show_pending', 'all')
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
