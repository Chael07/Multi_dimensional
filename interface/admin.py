from django.contrib import admin
from .models import Contact
from .models import Household

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'message')
    search_fields = ('first_name', 'email', 'message')

admin.site.register(Contact, ContactAdmin)

# this is for the evaluation
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ('id', 'mpi', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13')
    search_fields = ('id','mpi', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13')

admin.site.register(Household, HouseholdAdmin)