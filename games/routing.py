from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('games/<str:board_code>/updater/', consumers.BoardUpdateConsumer)
]