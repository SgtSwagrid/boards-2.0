from django.contrib import admin
from django.urls import include, path
from base import views

urlpatterns = [
    path('', views.index_view),
    path('admin/', admin.site.urls),
    path('games/', include('games.urls')),
    path('users/', include('users.urls'))
]