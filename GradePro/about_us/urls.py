from django.urls import path
from .views import about_us

urlpatterns = [
    path("aboutus/", about_us, name="aboutus_page")  
]
