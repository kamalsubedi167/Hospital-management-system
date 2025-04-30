from django import forms
from .models import Patient, Doctor, Appointment, Medicine, LabReport,Billing

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender',
            'marital_status', 'nationality', 'primary_phone', 'secondary_phone', 'email',
            'address_street', 'address_city', 'address_state', 'address_postal', 'address_country',
            'permanent_address_same', 'emergency_contact_name', 'emergency_contact_relationship',
            'emergency_contact_phone', 'blood_group', 'doctor', 'allergies', 'chronic_conditions',
            'current_medications', 'insurance_provider', 'insurance_policy_number',
            'billing_address_same', 'consent_for_treatment'
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(),
            'marital_status': forms.Select(),
            'blood_group': forms.Select(),
            'emergency_contact_relationship': forms.Select(),
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'chronic_conditions': forms.Textarea(attrs={'rows': 3}),
            'current_medications': forms.Textarea(attrs={'rows': 3}),
            'doctor': forms.Select(),
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'department', 'experience_years']
        widgets = {
            'experience_years': forms.NumberInput(attrs={'min': 0}),
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'appointment_date']
        widgets = {
            'appointment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'patient': forms.Select(),
            'doctor': forms.Select(),
        }

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'type', 'stock', 'price']
        widgets = {
            'stock': forms.NumberInput(attrs={'min': 0}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

class LabReportForm(forms.ModelForm):
    class Meta:
        model = LabReport
        fields = ['patient', 'test_name', 'result', 'is_pending']
        widgets = {
            'patient': forms.Select(),
            'result': forms.Textarea(attrs={'rows': 3}),
            'is_pending': forms.CheckboxInput(),
        }
class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['patient', 'amount', 'bill_date', 'is_paid', 'description']
        widgets = {
            'bill_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
