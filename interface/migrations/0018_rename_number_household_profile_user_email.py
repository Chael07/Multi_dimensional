# Generated by Django 4.1.3 on 2023-12-05 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0017_rename_c_number_household_profile_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='household_profile',
            old_name='number',
            new_name='user_email',
        ),
    ]