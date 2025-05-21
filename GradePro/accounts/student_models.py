
from django.db import models
from .models import Profile   

class StudentProfile(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    