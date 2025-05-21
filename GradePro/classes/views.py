from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy    
from django.contrib.auth import login, authenticate
from .forms import ClassCreateForm
from django.shortcuts import render
from classes.models import Grades
from accounts.student_models import StudentProfile

# Create your views here.
def home_page(request):
    if not request.user.is_authenticated:
        return redirect('register')
    return render(request, "classes/home.html")

class ClassCreateView(FormView):
    template_name = 'classes/create_class.html'
    form_class = ClassCreateForm
    success_url = reverse_lazy('home_page')  # change this

    def form_valid(self, form):
        class_obj = form.save()
        return super().form_valid(form)



def profile_page(request):
    student_profile = request.user.studentprofile
    subjects = student_profile.students.all()

    subject_data = {}

    for subject in subjects:
        grades_for_this_subject = []

        # get all Grades objects related to this class
        related_grades = Grades.objects.filter(school_class=subject)

        for grade_entry in related_grades:
            grades_for_this_subject.extend(grade_entry.values)

        average = round(sum(grades_for_this_subject) / len(grades_for_this_subject), 2) if grades_for_this_subject else None

        subject_data[subject] = {
            "grades": grades_for_this_subject,
            "average": average
        }

    return render(request, "classes/profile.html", {
        "student": student_profile,
        "subject_data": subject_data
    })
