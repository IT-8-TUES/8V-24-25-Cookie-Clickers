from django import forms
from . import models

class ClassCreateForm(forms.ModelForm):
    class Meta:
        model = models.Class
        fields = ['students', 'subject']
        
        students_checkbox = forms.ModelMultipleChoiceField(
            queryset = models.StudentProfile.objects.all(),
            widget = forms.CheckboxSelectMultiple,
            required = False
        )
        