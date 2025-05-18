from django.shortcuts import render, redirect

# Create your views here.
def home_page(request):
    if not request.user.is_authenticated:
        return redirect('register')
    return render(request, "classes/home.html")