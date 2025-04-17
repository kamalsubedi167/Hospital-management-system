from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'middle_name', 'last_name', 'date_of_birth', 'gender',
            'marital_status', 'nationality', 'primary_phone', 'secondary_phone', 'email',
            'address_street', 'address_city', 'address_state', 'address_postal', 'address_country',
            'permanent_address_same', 'emergency_contact_name', 'emergency_contact_relationship',
            'emergency_contact_phone', 'blood_group', 'allergies', 'chronic_conditions',
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
            'consent_for_treatment': forms.CheckboxInput(),
            'permanent_address_same': forms.CheckboxInput(),
            'billing_address_same': forms.CheckboxInput(),
        }
