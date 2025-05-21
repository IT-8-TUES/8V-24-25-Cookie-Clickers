from django import forms
from . import models


class ClassCreateForm(forms.ModelForm):
    class Meta:
        model = models.Class
        fields = ['subject', 'students']

    students = forms.ModelMultipleChoiceField(
        queryset = models.StudentProfile.objects.all(),
        widget = forms.SelectMultiple(attrs={'id': 'id_students'}),
        required = False
    )

        