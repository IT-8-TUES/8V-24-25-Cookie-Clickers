from django.db import models
from accounts.models import StudentProfile

# Create your models here.
class Class(models.Model):
    subject = models.CharField(max_length=50)
    students = models.ManyToManyField(StudentProfile, related_name='students')
    
