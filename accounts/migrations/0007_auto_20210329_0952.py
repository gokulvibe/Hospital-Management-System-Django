# Generated by Django 3.1.7 on 2021-03-29 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_doctorprofile_date_of_joining'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/doctor_profile_picture/'),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/patient_profile_picture/'),
        ),
        migrations.AlterField(
            model_name='staffprofile',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pictures/staff_profile_picture/'),
        ),
    ]
