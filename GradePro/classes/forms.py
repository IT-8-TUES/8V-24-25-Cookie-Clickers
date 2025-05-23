# forms.py

from django import forms
from .models import Class, StudentProfile
from .models import TeacherProfile  # adjust if needed

class ClassCreateForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['subject', 'school', 'students']  # 'teacher' is set manually

    students = forms.ModelMultipleChoiceField(
        queryset=StudentProfile.objects.all(),
        widget=forms.SelectMultiple(attrs={'id': 'id_students'}),
        required=False
    )


        