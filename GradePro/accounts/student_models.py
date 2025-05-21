
from django.db import models
from .models import Profile   

class StudentProfile(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    grades = models.ManyToManyField('classes.Grades', related_name='grades', blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
