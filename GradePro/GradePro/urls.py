from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include("accounts.urls")),
    path('/', include("classes.urls")),
    path('info/', include("about_us.urls"))
]
