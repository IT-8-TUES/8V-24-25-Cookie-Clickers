from django.urls import path
from .views import home_page, ClassCreateView

urlpatterns = [
    path("", home_page, name="home_page"),
    path("class_create/", ClassCreateView.as_view(), name="create_class"),
]