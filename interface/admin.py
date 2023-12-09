from django.contrib import admin
from .models import Contact
from .models import Household 
from .models import Contact_Developer
from .models import HouseholdProfile, result_classify, ResultMPI
# for the comments or contact
class ContactAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'message', 'submission_time')  
    search_fields = ('first_name', 'email', 'message', 'submission_time')  

admin.site.register(Contact, ContactAdmin)

class Contact_DeveloperAdmin(admin.ModelAdmin):
    list_display = ('name_admin', 'issue', 'messages')
    search_fields = ('name_admin', 'issue', 'messages')

admin.site.register(Contact_Developer, Contact_DeveloperAdmin)


# this is for the evaluation
class HouseholdAdmin(admin.ModelAdmin):
    list_display = ('id', 'indi1', 'indi2', 'indi3', 'indi4', 'indi5', 'indi6', 'indi7', 'indi8', 'indi9', 'indi10', 'indi11', 'indi12', 'indi13')
    search_fields = ('id', 'indi1', 'indi2', 'indi3', 'indi4', 'indi5', 'indi6', 'indi7', 'indi8', 'indi9', 'indi10', 'indi11', 'indi12', 'indi13')

admin.site.register(Household, HouseholdAdmin)

class HouseholdProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'user_number', 'user_email', 'user_address',)
    search_fields = ('id', 'first_name', 'last_name', 'user_number', 'user_email', 'user_address',)
admin.site.register(HouseholdProfile, HouseholdProfileAdmin)

class result_classify_admin(admin.ModelAdmin):
    list_display =('id', 'svm_result',)
    list_display =('id', 'svm_result',)

admin.site.register(result_classify, result_classify_admin)

class result_mpi_admin(admin.ModelAdmin):
    list_display =('id', 'mpi',)
    list_display =('id', 'mpi',)
admin.site.register(ResultMPI, result_mpi_admin)