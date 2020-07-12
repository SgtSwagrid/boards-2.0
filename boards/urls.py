from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('games/', include('games.urls')),
    path('users/', include('users.urls'))
]