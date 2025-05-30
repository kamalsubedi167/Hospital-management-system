# Generated by Django 5.2 on 2025-04-17 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient_id', models.CharField(editable=False, max_length=10, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('middle_name', models.CharField(blank=True, max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('marital_status', models.CharField(blank=True, choices=[('S', 'Single'), ('M', 'Married'), ('D', 'Divorced'), ('W', 'Widowed'), ('O', 'Other')], max_length=1)),
                ('nationality', models.CharField(blank=True, max_length=100)),
                ('primary_phone', models.CharField(max_length=15)),
                ('secondary_phone', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('address_street', models.CharField(max_length=200)),
                ('address_city', models.CharField(max_length=100)),
                ('address_state', models.CharField(max_length=100)),
                ('address_postal', models.CharField(max_length=20)),
                ('address_country', models.CharField(max_length=100)),
                ('permanent_address_same', models.BooleanField(default=True)),
                ('emergency_contact_name', models.CharField(max_length=100)),
                ('emergency_contact_relationship', models.CharField(choices=[('P', 'Parent'), ('S', 'Spouse'), ('B', 'Sibling'), ('F', 'Friend'), ('O', 'Other')], max_length=1)),
                ('emergency_contact_phone', models.CharField(max_length=15)),
                ('blood_group', models.CharField(choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'), ('U', 'Unknown')], default='U', max_length=3)),
                ('allergies', models.TextField(blank=True, default='None')),
                ('chronic_conditions', models.TextField(blank=True, default='None')),
                ('current_medications', models.TextField(blank=True, default='None')),
                ('insurance_provider', models.CharField(blank=True, default='Self-Pay', max_length=100)),
                ('insurance_policy_number', models.CharField(blank=True, max_length=50)),
                ('billing_address_same', models.BooleanField(default=True)),
                ('consent_for_treatment', models.BooleanField(default=False)),
            ],
        ),
    ]
