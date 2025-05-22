# forms.py

from django import forms
from .models import Class, StudentProfile
from .models import TeacherProfile  # adjust if needed

class ClassCreateForm(forms.ModelForm):
    teacher_email = forms.EmailField(label="Teacher Email")  # New field

    class Meta:
        model = Class
        fields = ['subject', 'school', 'students']  # 'teacher' is set manually

    students = forms.ModelMultipleChoiceField(
        queryset=StudentProfile.objects.all(),
        widget=forms.SelectMultiple(attrs={'id': 'id_students'}),
        required=False
    )

    def clean_teacher_email(self):
        email = self.cleaned_data['teacher_email']
        try:
            teacher = TeacherProfile.objects.get(user__email=email)
        except TeacherProfile.DoesNotExist:
            raise forms.ValidationError("No teacher found with this email.")
        return teacher  # Return the TeacherProfile instance


        