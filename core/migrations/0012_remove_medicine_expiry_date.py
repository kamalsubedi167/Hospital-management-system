# Generated by Django 5.2 on 2025-05-01 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_patient_allergies_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='expiry_date',
        ),
    ]
