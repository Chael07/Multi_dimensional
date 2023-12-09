# Generated by Django 4.1.3 on 2023-12-09 08:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0032_remove_result_classify_dt_result'),
    ]

    operations = [
        migrations.CreateModel(
            name='HouseholdProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('user_number', models.CharField(max_length=255)),
                ('user_address', models.CharField(max_length=255)),
                ('user_email', models.CharField(max_length=50, validators=[django.core.validators.MaxValueValidator(99999999999)])),
            ],
        ),
        migrations.CreateModel(
            name='ResultMPI',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mpi', models.FloatField(default=0.0)),
            ],
        ),
        migrations.DeleteModel(
            name='household_profile',
        ),
        migrations.AddField(
            model_name='householdprofile',
            name='mpi',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='interface.resultmpi'),
        ),
    ]