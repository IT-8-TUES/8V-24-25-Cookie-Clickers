from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from django.urls import reverse_lazy    
from django.contrib.auth import login, authenticate
from .forms import ClassCreateForm

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
    if not request.user.is_authenticated:
        return redirect('register')
    return render(request, "classes/profile.html")
