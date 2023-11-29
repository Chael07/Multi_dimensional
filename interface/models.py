from django.db import models
import pandas as pd

# Create your models here.
class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.first_name

    