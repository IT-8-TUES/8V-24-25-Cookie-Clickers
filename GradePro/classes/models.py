from django.db import models
from accounts.student_models import StudentProfile, TeacherProfile

class School(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

# Create your models here.
class Class(models.Model):
    subject = models.CharField(max_length=50)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='classes')
    students = models.ManyToManyField(StudentProfile, related_name='enrolled_classes')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='school')
    
    def __str__(self):
        return f"{self.subject} в {self.school.name}"
    
class Grades(models.Model):
    values = models.JSONField(default=list, blank=True)
    school_class = models.ManyToManyField(Class, related_name="classes")
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name="student_grade", null=True)

    
