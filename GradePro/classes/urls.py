from django.urls import path
from .views import home_page,hero_page, profile_page, ClassCreateView
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("", hero_page, name="hero_page"),  # unified hero page view
    path("home/", home_page, name="home_page"),  # unified home page view
    path("class_create/", ClassCreateView.as_view(), name="create_class"),
    path("profile/", profile_page, name="profile_page"),
    path('classes/<int:class_id>/students/', views.get_class_students, name='get_students'),
    path('classes/<int:class_id>/students/<int:student_id>/grades/', views.get_student_grades, name='get_grades'),
    path('assign_grade/', views.assign_grade, name='assign_grade'),
    path('get_students/<int:class_id>/', views.get_class_students, name='get_students'),
    path('view_classes/', views.view_classes,name='view_classes'),
]