from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from .models import Profile
from .student_models import StudentProfile, TeacherProfile

class UserRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = 'http://127.0.0.1:8000/account/login/'  

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user_type = form.cleaned_data['user_type']
        if user_type == 'teacher':
            user.is_teacher = True
            user.save()
            TeacherProfile.objects.create(user=user)
        else:
            user.is_teacher = False
            user.save()
            StudentProfile.objects.create(user=user)
        redirect('login')
        

        return super().form_valid(form)
     
class UserLoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
            return redirect('home_page')
        else:
            form.add_error(None, "Invalid email or password.")
            return self.form_invalid(form)
