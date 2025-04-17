from django.db import models
from django.utils import timezone
from datetime import date

class Patient(models.Model):
    # Basic Information
    patient_id = models.CharField(max_length=10, unique=True, editable=False)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
        ('O', 'Other'),
    ]
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES, blank=True)
    nationality = models.CharField(max_length=100, blank=True)

    # Contact Information
    primary_phone = models.CharField(max_length=15)
    secondary_phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address_street = models.CharField(max_length=200)
    address_city = models.CharField(max_length=100)
    address_state = models.CharField(max_length=100)
    address_postal = models.CharField(max_length=20)
    address_country = models.CharField(max_length=100)
    permanent_address_same = models.BooleanField(default=True)

    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=100)
    RELATIONSHIP_CHOICES = [
        ('P', 'Parent'),
        ('S', 'Spouse'),
        ('B', 'Sibling'),
        ('F', 'Friend'),
        ('O', 'Other'),
    ]
    emergency_contact_relationship = models.CharField(max_length=1, choices=RELATIONSHIP_CHOICES)
    emergency_contact_phone = models.CharField(max_length=15)

    # Medical Information
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('U', 'Unknown'),
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, default='U')
    allergies = models.TextField(blank=True, default='None')
    chronic_conditions = models.TextField(blank=True, default='None')
    current_medications = models.TextField(blank=True, default='None')

    # Insurance and Billing
    insurance_provider = models.CharField(max_length=100, blank=True, default='Self-Pay')
    insurance_policy_number = models.CharField(max_length=50, blank=True)
    billing_address_same = models.BooleanField(default=True)

    # Legal and Consent
    consent_for_treatment = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            self.patient_id = f'P{timezone.now().strftime("%Y%m%d")}{Patient.objects.count() + 1:04d}'
        super().save(*args, **kwargs)

    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
