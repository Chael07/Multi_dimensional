# Generated by Django 4.1.3 on 2023-11-29 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interface', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Household',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('q1', models.CharField(max_length=3)),
                ('q2', models.CharField(max_length=3)),
                ('q3', models.CharField(max_length=3)),
                ('q4', models.CharField(max_length=3)),
                ('q5', models.CharField(max_length=3)),
                ('q6', models.CharField(max_length=3)),
                ('q7', models.CharField(max_length=3)),
                ('q8', models.CharField(max_length=3)),
                ('q9', models.CharField(max_length=3)),
                ('q10', models.CharField(max_length=3)),
                ('q11', models.CharField(max_length=3)),
                ('q12', models.CharField(max_length=3)),
                ('q13', models.CharField(max_length=3)),
            ],
        ),
    ]
