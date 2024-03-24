import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

@login_required(login_url="/login")
def games(request):
    return render(request, 'main/games.html')

def snake(request):
    return render(request, "snake/snake.html")


def guess(request):
    return render(request, "games/numguess.html")