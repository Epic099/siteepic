from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/guess/', consumers.GuessConsumer.as_asgi())
]