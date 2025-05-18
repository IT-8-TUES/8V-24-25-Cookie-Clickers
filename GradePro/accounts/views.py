from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm
from .models import StudentProfile, TeacherProfile, Profile

class UserRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = 'http://127.0.0.1:8000/account/login/'  

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        user_type = form.cleaned_data['user_type']
        if user_type == 'student':
            StudentProfile.objects.create(user=user)
        else:
            TeacherProfile.objects.create(user=user)
        redirect('login')

        return super().form_valid(form)
     
class UserLoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    
    def form_valid(self, form):
        first_name=form.cleaned_data['first_name']
        last_name=form.cleaned_data['last_name']
        password = form.cleaned_data['password']
        
        user = Profile.objects.filter(
            first_name=first_name, 
            last_name=last_name, 
        ).first()
        if user is None:
            form.add_error(None, "Invalid first or last name!")
            return self.form_invalid(form)
        
        if user.check_password(password):
            login(self.request, user)
            return redirect('home_page')
        else:
            form.add_error(None, "Невалидна парола.")
            return self.form_invalid(form)
