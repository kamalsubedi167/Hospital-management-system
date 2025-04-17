from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient
from .forms import PatientForm

def home(request):
    return render(request, 'home.html')

@login_required
def patient_list(request):
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
