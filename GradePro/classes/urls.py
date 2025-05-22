from django.urls import path
from .views import home_page, profile_page, ClassCreateView
from django.views.generic import TemplateView


urlpatterns = [
    path("", home_page, name="home_page"),
    path("class_create/", ClassCreateView.as_view(), name="create_class"),
    path("profile/", profile_page, name="profile_page"),
]