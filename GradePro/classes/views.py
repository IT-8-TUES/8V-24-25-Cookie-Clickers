from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy    
from django.contrib.auth import login, authenticate
from .forms import ClassCreateForm
from django.shortcuts import render
from classes.models import Grades, Class
from accounts.student_models import StudentProfile, TeacherProfile
from .models import School
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
        school = School.objects.get(name="SigmaSchoolTSTS")
        teacher_profile = TeacherProfile.objects.get(user=self.request.user)
        class_obj = form.save(commit=False)
        class_obj.school = school
        class_obj.teacher = teacher_profile            
        class_obj.save()
        form.save_m2m()    
        return super().form_valid(form)



def profile_page(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    tab = request.GET.get("tab", "grades")
    cls_id = request.GET.get("class")  # for ranking

    subjects = student_profile.enrolled_classes.all().select_related("school")

    subject_data = {}
    overall_values = []

    for subject in subjects:
        grades_qs = Grades.objects.filter(student=student_profile, school_class=subject)
        values = []
        for grade in grades_qs:
            values.extend(grade.values)

        avg = round(sum(values) / len(values), 2) if values else None
        subject_data[subject] = {
            "grades": values,
            "average": avg
        }
        overall_values.extend(values)

    overall_avg = round(sum(overall_values) / len(overall_values), 2) if overall_values else None

    # ─────── Ranking only in current class ───────
    ranking = None
    place = None
    selected_class = None

    if tab == "rank":
        selected_class = get_object_or_404(Class, id=cls_id) if cls_id else subjects.first()
        classmates = selected_class.students.all()

        ranking = []
        for mate in classmates:
            mate_grades = Grades.objects.filter(student=mate, school_class=selected_class)
            mate_values = []
            for g in mate_grades:
                mate_values.extend(g.values)

            avg = round(sum(mate_values) / len(mate_values), 2) if mate_values else 0
            ranking.append((mate, avg))

        ranking.sort(key=lambda x: x[1], reverse=True)

        for idx, (mate, _) in enumerate(ranking, start=1):
            if mate.id == student_profile.id:
                place = idx
                break

    return render(request, "classes/profile.html", {
        "student": student_profile,
        "subject_data": subject_data,
        "overall_avg": overall_avg,
        "ranking": ranking,
        "place": place,
        "active_tab": tab,
        "subjects": subjects,
        "selected_class": selected_class,
    })
