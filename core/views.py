from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patient
from .forms import PatientForm
from django.db.models import Q

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
