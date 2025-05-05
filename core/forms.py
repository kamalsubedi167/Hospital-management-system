from django import forms
from django.utils import timezone
from datetime import date
from .models import Patient, Doctor, Appointment, Medicine, LabReport, Billing

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

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        if dob > date.today():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return dob

    def clean_primary_phone(self):
        phone = self.cleaned_data['primary_phone']
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Primary phone must be exactly 10 digits.")
        return phone

    def clean_secondary_phone(self):
        phone = self.cleaned_data.get('secondary_phone')
        if phone and (not phone.isdigit() or len(phone) != 10):
            raise forms.ValidationError("Secondary phone must be exactly 10 digits.")
        return phone

    def clean_emergency_contact_phone(self):
        phone = self.cleaned_data['emergency_contact_phone']
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError("Emergency contact phone must be exactly 10 digits.")
        return phone

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

    def clean_appointment_date(self):
        appointment_date = self.cleaned_data['appointment_date']
        if appointment_date < timezone.now():
            raise forms.ValidationError("Appointment date cannot be in the past.")
        return appointment_date

class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'type', 'stock', 'price']
        widgets = {
            'stock': forms.NumberInput(attrs={'min': 0}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def clean_stock(self):
        stock = self.cleaned_data['stock']
        if stock < 0:
            raise forms.ValidationError("Stock cannot be negative.")
        return stock

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

class LabReportForm(forms.ModelForm):
    class Meta:
        model = LabReport
        fields = ['patient', 'test_name', 'result', 'is_pending','file']
        widgets = {
            'patient': forms.Select(),
            'result': forms.Textarea(attrs={'rows': 3}),
            'is_pending': forms.CheckboxInput(),
            'file': forms.ClearableFileInput(attrs={'accept': 'image/*,application/pdf,video/*'}),
        }

    def clean_date(self):
        report_date = self.cleaned_data['date']
        if report_date > timezone.now():
            raise forms.ValidationError("Report date cannot be in the future.")
        return report_date

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'mp4', 'avi', 'mov']
            extension = file.name.split('.')[-1].lower()
            if extension not in allowed_extensions:
                raise forms.ValidationError("File type not supported. Allowed types: images, PDFs, videos.")
            if file.size > 10 * 1024 * 1024:  # 10 MB limit
                raise forms.ValidationError("File size must be under 10 MB.")
        return file

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['patient', 'amount', 'bill_date', 'is_paid', 'description']
        widgets = {
            'bill_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

    def clean_bill_date(self):
        bill_date = self.cleaned_data['bill_date']
        if bill_date > timezone.now().date():
            raise forms.ValidationError("Bill date cannot be in the future.")
        return bill_date
