from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class ProfileManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

class Profile(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.CharField(max_length=100, default="student")

    USERNAME_FIELD = 'email'

    objects = ProfileManager()

class StudentProfile(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    grades = models.JSONField(default=list, blank=True)

class TeacherProfile(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)