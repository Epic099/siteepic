from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/chess/<str:room>/', consumers.ChessConsumer.as_asgi()),
    path(r'ws/guess/', consumers.GuessConsumer.as_asgi())
]