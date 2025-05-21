from django.contrib import admin
from .models import Profile
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin


admin.site.register(Profile)