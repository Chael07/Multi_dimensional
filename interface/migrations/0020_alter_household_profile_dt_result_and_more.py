# Generated by Django 4.1.3 on 2023-12-05 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0019_alter_household_profile_dt_result_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household_profile',
            name='dt_result',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='household_profile',
            name='svm_result',
            field=models.FloatField(blank=True, null=True),
        ),
    ]