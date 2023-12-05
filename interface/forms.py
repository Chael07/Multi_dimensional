from django import forms
from .models import Household

class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = '__all__'


class email_forgot_pass(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Please enter your email here'})
    )