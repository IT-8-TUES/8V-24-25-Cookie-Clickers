# accounts/forms.py
from django import forms
from . import models

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = models.Profile
        fields = ['first_name', 'last_name', 'email', 'password']
        
class UserLoginForm(forms.Form):
    first_name = forms.CharField(label="Име")
    last_name = forms.CharField(label="Фамилия")
    password = forms.CharField(widget=forms.PasswordInput, label="Парола")