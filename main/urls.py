from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("games", views.games, name="games"),
    path("chess", views.chessrooms, name="chess-rooms"),
    path("chess/<str:room_name>", views.chess, name="chess"),
    path("snake", views.snake, name="snake"),
    path("games/numguess", views.guess, name="guess"),
]
