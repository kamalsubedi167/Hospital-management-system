from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Patient

def home(request):
    return render(request, 'home.html')

@login_required
def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})
