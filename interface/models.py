from django.db import models
import pandas as pd
from django.contrib.auth.models import User

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.first_name

class Contact_Developer(models.Model):
    name_admin = models.CharField(max_length=255)
    issue = models.EmailField()
    messages = models.TextField()

    def __str__(self):
        return self.first_name

class Household(models.Model):
    mpi = models.FloatField(default=0.0)
    q1 = models.FloatField()
    q2 = models.FloatField()
    q3 = models.FloatField()
    q4 = models.FloatField()
    q5 = models.FloatField()
    q6 = models.FloatField()
    q7 = models.FloatField()
    q8 = models.FloatField()
    q9 = models.FloatField()
    q10 = models.FloatField()
    q11 = models.FloatField()
    q12 = models.FloatField()
    q13 = models.FloatField()


