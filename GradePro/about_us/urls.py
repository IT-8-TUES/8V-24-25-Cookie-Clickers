from django.urls import path
from .views import about_us

urlpatterns = [
    path("", about_us, name="aboutus_page")  
]
