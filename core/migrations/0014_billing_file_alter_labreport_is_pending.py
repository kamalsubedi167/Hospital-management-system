# Generated by Django 5.2 on 2025-05-05 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='lab_reports/'),
        ),
        migrations.AlterField(
            model_name='labreport',
            name='is_pending',
            field=models.BooleanField(choices=[(True, 'Pending'), (False, 'Completed')], default=True),
        ),
    ]
