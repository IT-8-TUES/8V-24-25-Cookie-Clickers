from django.contrib import admin
from .models import Class, StudentProfile, School, Grades, TeacherProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'id')

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    full_name.short_description = 'Name'

# Register your models here.
admin.site.register(Class)

admin.site.register(School)

admin.site.register(Grades)

admin.site.register(TeacherProfile)


