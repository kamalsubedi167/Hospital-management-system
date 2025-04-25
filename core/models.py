from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]
    RELATIONSHIP_CHOICES = [
        ('SPOUSE', 'Spouse'),
        ('PARENT', 'Parent'),
        ('CHILD', 'Child'),
        ('SIBLING', 'Sibling'),
        ('OTHER', 'Other'),
    ]
    patient_id = models.CharField(max_length=20, unique=True, blank=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    nationality = models.CharField(max_length=50, blank=True)
    primary_phone = models.CharField(max_length=15)
    secondary_phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    address_street = models.CharField(max_length=100)
    address_city = models.CharField(max_length=50)
    address_state = models.CharField(max_length=50)
    address_postal = models.CharField(max_length=10)
    address_country = models.CharField(max_length=50)
    permanent_address_same = models.BooleanField(default=True)
    emergency_contact_name = models.CharField(max_length=100)
    emergency_contact_relationship = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES)
    emergency_contact_phone = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    doctor = models.ForeignKey('Doctor', on_delete=models.SET_NULL, null=True, blank=True)
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_policy_number = models.CharField(max_length=50, blank=True)
    billing_address_same = models.BooleanField(default=True)
    consent_for_treatment = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.patient_id:
            last_patient = Patient.objects.order_by('-id').first()
            if last_patient:
                last_id = int(last_patient.patient_id.split('-')[1])
                new_id = last_id + 1
            else:
                new_id = 1
            self.patient_id = f"P-{new_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    experience_years = models.IntegerField()
    user = models.OneToOneField('auth.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()

    def __str__(self):
        return f"Appointment with {self.doctor} for {self.patient} on {self.appointment_date}"

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class LabReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    result = models.TextField()
    is_pending = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test_name} for {self.patient}"
