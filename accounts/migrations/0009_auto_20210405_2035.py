# Generated by Django 3.1.7 on 2021-04-05 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20210405_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='doctor_id',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='patient_id',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='staffprofile',
            name='staff_id',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]