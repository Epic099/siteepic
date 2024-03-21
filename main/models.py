from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class ChessRoom(models.Model):
    name = models.CharField(max_length=50)
    white = models.ForeignKey(User, on_delete=models.CASCADE, related_name="whiteuser", blank=True, null=True)
    black = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blackuser", blank=True, null=True)
    viewers = models.ManyToManyField(User, related_name="viewerslist", blank=True, null=True)
    Board = models.CharField(max_length=72, default="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    Color = models.BooleanField(default=False)
    Moves = models.CharField(max_length=10000, blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.name}"
    
class GuessRoom(models.Model):
    roomId = models.CharField(max_length=6)
    player1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player1", blank=True, null=True)
    player2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="player2", blank=True, null=True)
    number1 = models.CharField(max_length=3, blank=True, null=True)
    number2 = models.CharField(max_length=3, blank=True, null=True)
    turn = models.IntegerField(default=1)
    
    def __str__(self) -> str:
        return f"{self.roomId}"