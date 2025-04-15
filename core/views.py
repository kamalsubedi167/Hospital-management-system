from django.shortcuts import render
from .models import Patient #added this
# Create your views here.
def home(request):
    return render(request, 'home.html')
def patient_list(request):  # Add this
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})
