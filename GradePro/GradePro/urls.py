from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include("accounts.urls")),
    path('', include("classes.urls")),
    path('aboutus/', include("about_us.urls")),
]
