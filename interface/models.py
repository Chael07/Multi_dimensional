from django.db import models
import uuid
from django.core.validators import MaxValueValidator

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submission_time = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.first_name
    
class Contact_Developer(models.Model):
    name_admin = models.CharField(max_length=255)
    issue = models.EmailField()
    messages = models.TextField()

    def __str__(self):
        return self.first_name
    
class Household(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
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

    def __str__(self):
        return f"Household {self.id}"

class household_profile(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_email = models.CharField(max_length=11, validators=[MaxValueValidator(99999999999)])
    mpi = models.FloatField(default=0.0)

    def __str__(self):
        return f"Household {self.id}"

class result_classify(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    dt_result = models.FloatField()
    svm_result = models.FloatField()

    def __str__(self):
        return str(self.id)