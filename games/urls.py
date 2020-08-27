from django.urls import path
from . import views

urlpatterns = [

    path('', views.browse_view),
    path('create/', views.create_view),

    path('<str:board_code>/board/', lambda request, board_code:
        views.board_view(request, board_code, -1)),
    path('<str:board_code>/board/<int:state_id>/', views.board_view),

    path('<str:board_code>/sidebar/', lambda request, board_code:
        views.sidebar_view(request, board_code, -1)),
    path('<str:board_code>/sidebar/<int:state_id>/', views.sidebar_view),

    path('<str:board_code>/fork/<int:state_id>/', views.fork_view),
    path('<str:board_code>/rematch/', views.rematch_view),

    path('<str:board_code>/', lambda request, board_code:
        views.game_view(request, board_code, -1)),
    path('<str:board_code>/<int:state_id>/', views.game_view)
]