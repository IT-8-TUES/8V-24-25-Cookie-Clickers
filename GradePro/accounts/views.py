from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import UserRegistrationForm
from .models import StudentProfile, TeacherProfile

class UserRegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('')  # Change to your desired URL

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()

        user_type = form.cleaned_data['user_type']
        if user_type == 'student':
            StudentProfile.objects.create(user=user)
        else:
            TeacherProfile.objects.create(user=user)

        login(self.request, user)
        return super().form_valid(form)
