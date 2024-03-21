from enum import Enum

    
class Flags(Enum):
    Capture = 1
    PawnTwoMove = 2
    
class Pieces():
    Empty = 0
    Pawn = 1
    Bishop = 2
    Knight = 3
    Rook = 4
    Queen = 5
    King = 6

class Color(Enum):
    Colorless = 0
    White = 1
    Black = 2

class Vector2():
    def __init__(self, x : int, y : int) -> None:
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"{self.x} {self.y}"
        
class Move():
    def __init__(self, startSquare : int, targetSquare : int, startPiece : int = Pieces.Empty, targetPiece : int = Pieces.Empty,startColor : int = Color.Colorless, flag : Flags = 0) -> None:        
        self.startSquare = startSquare
        self.targetSquare = targetSquare
        self.startPiece = startPiece
        self.targetPiece = targetPiece
        self.startColor = startColor
        self.flag = flag
    def isLegal(self, legalMoves):
        for move in legalMoves:
            if self.startSquare == move.startSquare and self.targetSquare == move.targetSquare:
                return True
        return False
    def __str__(self):
        return f"{self.startSquare} {self.targetSquare}"
    

        
class Piece():
    def __init__(self, typ : Pieces = Pieces.Empty, color : Color = Color.Colorless):
        self.typ = typ
        self.isSlidingPeace = False
        self.color = color
        if typ in [Pieces.Bishop, Pieces.Queen, Pieces.Rook]:
            self.isSlidingPeace = True
    def isColor(self, color):
        return self.color == color
    def getEnemyColor(self):
        if self.color == Color.White:
            return Color.Black
        elif self.color == Color.Black:
            return Color.White
    def isType(self, typ : Pieces):
        return self.typ == typ

    def __str__(self) -> str:
        return f"{self.typ} ({self.color})"
        