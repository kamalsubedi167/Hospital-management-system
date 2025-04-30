from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Patient(models.Model):
    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    RELATIONSHIP_CHOICES = [
        ('SPOUSE', 'Spouse'),
        ('PARENT', 'Parent'),
        ('CHILD', 'Child'),
        ('SIBLING', 'Sibling'),
        ('OTHER', 'Other'),
    ]
    patient_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    nationality = models.CharField(max_length=50)
    primary_phone = models.CharField(max_length=15)
    address_street = models.CharField(max_length=100)
    address_city = models.CharField(max_length=50)
    address_state = models.CharField(max_length=50)
    address_postal = models.CharField(max_length=10)
    address_country = models.CharField(max_length=50)
    permanent_address_same = models.BooleanField(default=True)
    permanent_street = models.CharField(max_length=100, blank=True, null=True)
    permanent_city = models.CharField(max_length=50, blank=True, null=True)
    permanent_state = models.CharField(max_length=50, blank=True, null=True)
    permanent_postal = models.CharField(max_length=10, blank=True, null=True)
    permanent_country = models.CharField(max_length=50, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    emergency_contact_phone = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    consent_for_treatment = models.BooleanField(default=False)
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True)
#done for check
    created_at = models.DateTimeField(default=timezone.now) #testcheck
    insurance_policy_number = models.CharField(max_length=100)
    insurance_provider = models.CharField(max_length=100)
    current_medications = models.TextField()
    allergies = models.TextField()
    middle_name = models.CharField(max_length=100)
    secondary_phone = models.CharField(max_length=15)
    billing_address_same = models.BooleanField(default=False)
    chronic_conditions = models.TextField()
    email = models.EmailField()
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.patient_id})"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    experience_years = models.IntegerField()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment with {self.doctor} for {self.patient} on {self.appointment_date}"

class Medicine(models.Model):
    MEDICINE_TYPE_CHOICES = [
        ('TABLET', 'Tablet'),
        ('CAPSULE', 'Capsule'),
        ('SYRUP', 'Syrup'),
        ('INJECTION', 'Injection'),
        ('OTHER', 'Other'),
    ]
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=MEDICINE_TYPE_CHOICES)
    stock = models.IntegerField()
    expiry_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)#test
    def __str__(self):
        return f"{self.name} ({self.type})"

class LabReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    result = models.TextField()
    date = models.DateField(default=timezone.now)
    is_pending = models.BooleanField(default=True)

    def __str__(self):
        return f"Lab Report for {self.patient} - {self.test_name}"

class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill_date = models.DateField(default=timezone.now)
    is_paid = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Bill for {self.patient} - ${self.amount} ({'Paid' if self.is_paid else 'Unpaid'})"
class Diagnosis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    disease = models.CharField(max_length=100)
    diagnosis_date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Diagnosis of {self.disease} for {self.patient}"
