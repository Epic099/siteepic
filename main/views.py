import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from . import models
from .forms import ChessRoomForm
from . import chess as ChessAPI
from . import classes as ChessAPIConfig

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

@login_required(login_url="/login")
def games(request):
    return render(request, 'main/games.html')

@login_required(login_url="/login")
def chessrooms(request):
    rooms = models.ChessRoom.objects.all()
    room_names = []
    for room in rooms:
        room_names.append(room.name)
    form = ChessRoomForm()
    return render(request, 'chess/rooms.html', context={"Rooms" : room_names, "form" : form})

@login_required(login_url="/login")
def chess(request, room_name):
    room = models.ChessRoom.objects.get(name=room_name)
    if room.white == None:
        board = ChessAPI.Board()
        board.loadFEN(room.Board)
        moves = board.calcMoves(ChessAPIConfig.Color.White, False, jsonFormat=True)
        json_moves = json.dumps(moves, indent=4)
        room.Moves = json_moves
        room.white = request.user
    elif room.black == None and room.white != request.user:
        room.black = request.user
    room.save()
    color = 0
    if room.white == request.user:
        color = 1
    elif room.black == request.user:
        color = 2
    return render(request, 'chess/chess.html', context={'room' : room_name, "BoardFEN" : room.Board, "Moves" : room.Moves, "Color" : color})

def snake(request):
    return render(request, "snake/snake.html")


def guess(request):
    return render(request, "games/numguess.html")