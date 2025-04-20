from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, Appointment, Medicine, LabReport
from .forms import PatientForm
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
    pending_lab_reports = LabReport.objects.filter(is_pending=True).count()
    low_stock_medicines = Medicine.objects.filter(stock__lt=10).count()
    blood_group_counts = Patient.objects.values('blood_group').annotate(count=Count('blood_group')).order_by('blood_group')
    context = {
        'total_patients': total_patients,
        'total_doctors': total_doctors,
        'todays_appointments': todays_appointments,
        'pending_lab_reports': pending_lab_reports,
        'low_stock_medicines': low_stock_medicines,
        'blood_group_counts': blood_group_counts,
    }
    return render(request, 'dashboard.html', context)
