from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import ClassCreateForm
from classes.models import Grades, Class
from accounts.student_models import StudentProfile, TeacherProfile
from .models import School
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def home_page(request):
    if not request.user.is_authenticated:
        return redirect('register')
    context = {}
    if not request.user.is_teacher:
        student_profile = get_object_or_404(StudentProfile, user=request.user)
        subjects = student_profile.enrolled_classes.all().select_related("school")
        overall_values = []
        
        for subject in subjects:
            grades_qs = Grades.objects.filter(student=student_profile, school_class=subject)
            values = []
            
            for grade in grades_qs:
                if isinstance(grade.values, list):
                    values.extend(grade.values)
                elif isinstance(grade.values, (int, float)):  # Include float for decimal grades
                    values.append(grade.values)
            
            if values:  # Only calculate if grades exist
                subject_avg = round(sum(values) / len(values), 2)
                overall_values.extend(values)
        
        if overall_values:  # Only calculate if any grades exist
            overall_avg = round(sum(overall_values) / len(overall_values), 2)
        else:
            overall_avg = None
        
        context = {'overall_avg': overall_avg}
        print("Calculated overall_avg:", overall_avg)  # Debug print
        return render(request, "classes/home.html", context)
    else:
        return render(request, "classes/home.html")
    
def hero_page(request):
    return render(request, "classes/hero.html")

def view_classes(request):
    if request.user.is_teacher:
        classes = None
        teacher_profile = request.user.teacherprofile
        classes = Class.objects.filter(teacher=teacher_profile)
        return render(request, "classes/view_classes.html", {'classes': classes})
    else:
        return render(request, "classes/home.html")


class ClassCreateView(FormView):
    template_name = 'classes/create_class.html'
    form_class = ClassCreateForm
    success_url = reverse_lazy('home_page')

    def form_valid(self, form):
        print(self.request.POST)
        teacher_profile = TeacherProfile.objects.get(user=self.request.user)
        class_obj = form.save(commit=False)
        class_obj.teacher = teacher_profile
        class_obj.save()
        form.save_m2m()
        return super().form_valid(form)


def profile_page(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    tab = request.GET.get("tab", "grades")
    cls_id = request.GET.get("class")

    subjects = student_profile.enrolled_classes.all().select_related("school")

    subject_data = {}
    overall_values = []
    
    for subject in subjects:
        grades_qs = Grades.objects.filter(student=student_profile, school_class=subject)
        values = []
        for grade in grades_qs:
            if isinstance(grade.values, list):
                values.extend(grade.values)
            elif isinstance(grade.values, int):
                values.append(grade.values)

        avg = round(sum(values) / len(values), 2) if values else None
        subject_data[subject] = {
            "grades": values,
            "average": avg
        }
        overall_values.extend(values)

    overall_avg = round(sum(overall_values) / len(overall_values), 2) if overall_values else None

    # ─────── CLASS RANKING ───────
    ranking = None
    place = None
    selected_class = None

    if tab == "rank":
        if cls_id:
            try:
                selected_class = Class.objects.get(id=cls_id)
            except Class.DoesNotExist:
                selected_class = subjects.first()
        else:
            selected_class = subjects.first()

        if selected_class:
            classmates = selected_class.students.all()
            ranking = []
            for mate in classmates:
                mate_grades = Grades.objects.filter(student=mate, school_class=selected_class)
                mate_values = []
                for g in mate_grades:
                    if isinstance(g.values, list):
                        mate_values.extend(g.values)
                    elif isinstance(g.values, int):
                        mate_values.append(g.values)
                avg = round(sum(mate_values) / len(mate_values), 2) if mate_values else 0
                ranking.append((mate, avg))

            ranking.sort(key=lambda x: x[1], reverse=True)
            for idx, (mate, _) in enumerate(ranking, start=1):
                if mate.id == student_profile.id:
                    place = idx
                    break

    # ─────── SCHOOL RANKING ───────
    school_ranking = None
    school_place = None

    if tab == "rank_school":
        first_class = subjects.first()
        selected_school = first_class.school if first_class else None

        if selected_school:
            classmates = StudentProfile.objects.filter(enrolled_classes__school=selected_school).distinct()
            school_ranking = []

            for mate in classmates:
                mate_values = []
                mate_grades = Grades.objects.filter(student=mate)
                for g in mate_grades:
                    if isinstance(g.values, list):
                        mate_values.extend(g.values)
                    elif isinstance(g.values, int):
                        mate_values.append(g.values)
                avg = round(sum(mate_values) / len(mate_values), 2) if mate_values else 0
                school_ranking.append((mate, avg))

            school_ranking.sort(key=lambda x: x[1], reverse=True)
            for idx, (mate, _) in enumerate(school_ranking, start=1):
                if mate.id == student_profile.id:
                    school_place = idx
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
        "school_ranking": school_ranking,
        "school_place": school_place,
    })

def get_class_students(request, class_id):
    try:
        school_class = Class.objects.get(id=class_id)
    except Class.DoesNotExist:
        return JsonResponse({"error": "Class not found"}, status=404)
    class_name = Class.objects.get(id=class_id).subject
    students = school_class.students.all()
    data = []
    for s in students:
        grades_qs = Grades.objects.filter(student=s, school_class=school_class)
        grades = []
        for g in grades_qs:
            grades.append(g.values)
        data.append({
            "id": s.id,
            "name": s.user.get_full_name(),
            "grades": grades
        })
    return JsonResponse({"students": data})


def get_student_grades(request, student_id, class_id):
    # AJAX: return grades for a specific student in a class
    grades = Grades.objects.filter(student_id=student_id, school_class_id=class_id).order_by('-timestamp')
    data = [g.value for g in grades]
    return JsonResponse({"grades": data})


@csrf_exempt
def assign_grade(request):
    # AJAX POST: assign a new grade to a student
    if request.method == "POST":
        data = json.loads(request.body)
        student_id = data.get('student_id')
        class_id = data.get('class_id')
        grade_value = data.get('grade') 
        print("Received data:", data)
        # Validate values here if needed

        grade = Grades.objects.create(student_id=student_id, school_class_id=class_id, values=[grade_value])
        return JsonResponse({"success": True, "grade": grade.values})

    return JsonResponse({"error": "Invalid request"}, status=400)

def students_not_in_class(request, class_id):
    try:
        school_class = Class.objects.get(id=class_id)
        students_in_class = school_class.students.all()
        all_students = StudentProfile.objects.all()
        not_in_class = all_students.exclude(id__in=students_in_class.values_list('id', flat=True))
        
        student_data = [{"id": s.id, "name": s.user.get_full_name()} for s in not_in_class]
        return JsonResponse({"students": student_data})
    except Class.DoesNotExist:
        return JsonResponse({"error": "Class not found"}, status=404)

@csrf_exempt
def add_student_to_class(request):
    if request.method == "POST":
        data = json.loads(request.body)
        student_id = data.get("student_id")
        class_id = data.get("class_id")

        try:
            school_class = Class.objects.get(id=class_id)
        except Class.DoesNotExist:
            return JsonResponse({"success": False, "error": "Class not found"})

        try:
            student = StudentProfile.objects.get(id=student_id)
        except StudentProfile.DoesNotExist:
            return JsonResponse({"success": False, "error": "Student not found"})

        school_class.students.add(student)
        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Invalid request"})
