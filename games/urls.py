from django.urls import path
from . import views

urlpatterns = [
    path('', views.browse_view),
    path('create/', views.create_view),
    path('<str:board_code>/', views.game_view),
    path('<str:board_code>/board/', views.board_view)
]