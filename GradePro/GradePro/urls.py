from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include("accounts.urls")),
    path('', include("classes.urls")),
    path('aboutus/', include("about_us.urls")),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]
