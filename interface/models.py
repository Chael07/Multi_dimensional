from django.db import models
from django.core.validators import MaxValueValidator
from django.db import models


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
    indi1 = models.FloatField()
    indi2 = models.FloatField()
    indi3 = models.FloatField()
    indi4 = models.FloatField()
    indi5 = models.FloatField()
    indi6 = models.FloatField()
    indi7 = models.FloatField()
    indi8 = models.FloatField()
    indi9 = models.FloatField()
    indi10 = models.FloatField()
    indi11 = models.FloatField()
    indi12 = models.FloatField()
    indi13 = models.FloatField()

class ResultMPI(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    mpi = models.FloatField(default=0.0)

class HouseholdProfile(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    user_number = models.CharField(max_length=255)
    user_address = models.CharField(max_length=255)
    user_email = models.CharField(max_length=50, validators=[MaxValueValidator(99999999999)])

class result_classify(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    svm_result = models.FloatField()
