# Generated by Django 4.1.3 on 2023-12-05 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0025_rename_unique_id_household_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='household_profile',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='result_classify',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]