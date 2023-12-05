from django.contrib import admin
from .models import Contact
from .models import Household 
from .models import Contact_Developer
from .models import household_profile, result_classify
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
    list_display = ('id', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13')
    search_fields = ('id', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9', 'q10', 'q11', 'q12', 'q13')

admin.site.register(Household, HouseholdAdmin)

class household_profile_admin(admin.ModelAdmin):
    list_display =('id', 'first_name', 'last_name', 'user_email', 'mpi', )
    search_fields =('id', 'first_name', 'last_name', 'user_email', 'mpi',)

admin.site.register(household_profile, household_profile_admin)

class result_classify_admin(admin.ModelAdmin):
    list_display =('id', 'dt_result', 'svm_result',)
    list_display =('id', 'dt_result', 'svm_result',)

admin.site.register(result_classify, result_classify_admin)