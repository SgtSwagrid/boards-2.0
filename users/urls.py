from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register_view),
    path('login', views.login_view)
]