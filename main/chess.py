import math
from .classes import Vector2, Color, Pieces, Flags, Move, Piece


class Config():
    STARTFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
    FEN = {"P" : Pieces.Pawn, "B" : Pieces.Bishop, "N" : Pieces.Knight, "R" : Pieces.Rook, "Q" : Pieces.Queen, "K" : Pieces.King}
    PieceToFEN = {Pieces.Pawn : "P", Pieces.Bishop : "B", Pieces.Knight : "N", Pieces.Rook: "R", Pieces.Queen: "Q", Pieces.King: "K"}
    DIRECTIONOFFSETS = [8, -8, -1, 1, 7, -7, 9, -9]


class Square():
    def __init__(self, index : int) -> None:
        self.index = index
        self.piece = Piece()
    def createArray(size):
        result = []
        for i in range(0, size):
            result.append(Square(i))
        return result
    def setPeace(self, piece : Piece):
        self.piece = piece
    def __str__(self):
        return f"{self.index}: {self.piece}"


        
class Board():
    def __init__(self) -> None:
        self.SquareCount = 64
        self.Squares = Square.createArray(self.SquareCount)
        self.NumSquaresToEdge = self.calcNumToEdge()
        self.lastCalculatedMoves = []
        self.ColorToMove = Color.White
    def calcNumToEdge(self):
        result = [None]*self.SquareCount
        for file in range(0, 8):
            for rank in range(0, 8):
                north =  7 - rank
                south = rank
                west = file
                east = 7 - file
                
                index = rank * 8 + file
                
                result[index] = [
                    north, south, west, east, min(north, west), min(south, east), min(north, east), min(south, west)
                ]
        return result
    def changeColor(self):
        if self.ColorToMove == Color.White:
            self.ColorToMove = Color.Black
        else:
            self.ColorToMove = Color.White
        self.calcMoves(self.ColorToMove)
    def makeMove(self, move : Move, nextPlayer : bool = True, override : bool = False):
        if not override and not move.isLegal(self.lastCalculatedMoves):
            return False
        startpiece = move.startPiece if move.startPiece != Pieces.Empty else self.getSquarePiece(move.startSquare)
        startcolor = startpiece.color
        self.setSquarePiece(move.startSquare, Pieces.Empty, Color.Colorless)
        self.setSquarePiece(move.targetSquare, startpiece.typ, startpiece.color)
        if nextPlayer:
            self.changeColor()
        return True
    def unmakeMove(self, move : Move):
        self.setSquarePiece(move.startSquare, move.startPiece.typ, move.startPiece.color)
        self.setSquarePiece(move.targetSquare, move.targetPiece.typ, move.targetPiece.color)
    def loadFEN(self, FEN = Config.STARTFEN):
        self.Squares = Square.createArray(64)
        index = 0
        for char in FEN:
            if char.isnumeric():
                index += int(char)
                continue
            for piece in Config.FEN.keys():
                y = math.floor(index/8)
                nIndex = (8-y)*8+((index-8)-y*8)
                if piece == char:
                    self.setSquarePiece(nIndex, Config.FEN[piece], Color.White)
                elif str.lower(piece) == char:
                    self.setSquarePiece(nIndex, Config.FEN[piece], Color.Black)
            if char != "/":
                index += 1
    def saveFEN(self) -> str:
        result = ""
        temp = 0
        for i in range(0, len(self.Squares)):
            y = math.floor(i/8)
            x = i - y*8
            _y = 7-y
            index = _y*8 + x
            piece = self.getSquarePiece(index)
            if piece.typ == Pieces.Empty:
                temp += 1
                if x == 7:
                    result += str(temp) + "/"
                    temp = 0
                continue
            else:
                if temp > 0:
                    result += str(temp)
                    temp = 0
                char = Config.PieceToFEN[piece.typ]
                if piece.color == Color.Black:
                    char = str.lower(char)
                result += char
            if x == 7:
                result += "/"
                temp = 0
        return result
        
    def setSquarePiece(self, index : int, piece : Pieces, color : Color):
        square = self.getSquare(index)
        square.piece = Piece(piece, color)
        self.Squares[index] == square
    def getSquarePiece(self, index : int) -> Piece:
        square = self.getSquare(index)
        return square.piece
    def getSquare(self, index : int) -> Square:
        return self.Squares[index]
    def getCoordinatesByIndex(self, index : int):
        y = math.floor(index/8)
        x = index-(y*8)
        return Vector2(x,y)
    def getMoves(color : Color):
        pass
    def getKingPosition(self, color : Color):
        for i in range(0, self.SquareCount-1):
            piece = self.getSquarePiece(i)
            if piece.typ == Pieces.King and piece.color == color:
                return i
    def calcMoves(self, color : Color, save : bool = True, jsonFormat : bool = False) -> list[Move]:
        pseudoLegal = self.calcPseudoLegalMoves(color)
        opponentcolor = Color.White
        print(self.getSquarePiece(39))
        if color == opponentcolor:
            opponentcolor = Color.Black
        legalMoves : list[Move] = []
        for move in pseudoLegal:
            self.makeMove(move, nextPlayer=False, override=True)
            responses = self.calcPseudoLegalMoves(opponentcolor)
            kingPosition = self.getKingPosition(color)
            movelegal = True
            for response in responses:
                if response.flag == Flags.Capture and response.targetSquare == kingPosition:
                    movelegal = False
            if movelegal:
                legalMoves.append(move)
            
            self.unmakeMove(move)
        if len(legalMoves) == 0:
            print(opponentcolor, "won the Game")
        if save:
            self.lastCalculatedMoves = legalMoves.copy()
        if jsonFormat:
            jsonMoves = []
            for move in legalMoves:
                _color = "black" if move.startColor == Color.Black else "white"
                jsonMoves.append({
                    "startSquare" : move.startSquare,
                    "targetSquare" : move.targetSquare,
                    "startColor" : _color,
                })
            return jsonMoves
        else:
            return legalMoves
    def calcPseudoLegalMoves(self, color : Color) -> list[Move]:
        moves = []
        for i in range(0, self.SquareCount-1):
            square = self.getSquare(i)
            piece = square.piece
            if piece.typ == Pieces.Empty or piece.color != color:
                continue
            if piece.isSlidingPeace:
                calcmoves = self.calcSlidingMoves(i)
                if calcmoves != None:
                    moves += calcmoves
                continue
            if piece.typ == Pieces.King:
                calcmoves = self.calcKingMoves(i)
                if calcmoves != None:
                    moves += calcmoves
                continue
            if piece.typ == Pieces.Pawn:
                calcmoves = self.calcPawnMoves(i)
                if calcmoves != None:
                    moves += calcmoves
                continue
            if piece.typ == Pieces.Knight:
                calcmoves = self.calcKnightMoves(i)
                if calcmoves != None:
                    moves += calcmoves
                continue
        return moves
    def calcKnightMoves(self, index : int):
        moves = []
        piece = self.getSquarePiece(index)
        friendlycolor = piece.color
        opponentcolor = piece.getEnemyColor()
        directions = [17, 10, -6, -15, -17, -10, 6, 15]
        startPos = self.getCoordinatesByIndex(index)
        for dir in directions:
            targetSquare = index + dir
            if targetSquare < 0 or targetSquare > self.SquareCount-1:
                continue
            targetPos = self.getCoordinatesByIndex(targetSquare)
            difference = Vector2(abs(startPos.x - targetPos.x), abs(startPos.y - targetPos.y))
            if difference.x > 2 or difference.y > 2:
                continue
            targetPiece = self.getSquarePiece(targetSquare)
            if targetPiece.color == friendlycolor:
                continue
            else:
                if targetPiece.color == opponentcolor:
                    moves.append(Move(index, targetSquare, flag=Flags.Capture, startPiece=self.getSquarePiece(index), targetPiece=self.getSquarePiece(targetSquare)))
                else:
                    moves.append(Move(index, targetSquare, startPiece=self.getSquarePiece(index), targetPiece=self.getSquarePiece(targetSquare)))
        return moves
    def calcPawnMoves(self, index : int):
        moves = []
        piece = self.getSquarePiece(index)
        friendlycolor = piece.color
        opponentcolor = piece.getEnemyColor()
        forwardsquare = None
        twosquare = NotImplemented
        if friendlycolor == Color.White:
            forwardsquare = index + 8
            twosquare = index + 16
            if index > 55:
                return []
            forwardpiece = self.getSquarePiece(forwardsquare)
            if index in [8, 9, 10, 11, 12, 13, 14, 15]:
                targetSquare = twosquare
                targetPiece = self.getSquarePiece(targetSquare)
                if targetPiece.typ == Pieces.Empty and forwardpiece.typ == Pieces.Empty:
                    moves.append(Move(index, targetSquare, flag=Flags.PawnTwoMove, startPiece=self.getSquarePiece(index), targetPiece=self.getSquarePiece(targetSquare)))
            targetIndex = index + 7
            targetPiece = self.getSquarePiece(targetIndex)
            if targetPiece.color == opponentcolor:
                moves.append(Move(index, targetIndex, flag=Flags.Capture, startPiece=self.getSquarePiece(index), targetPiece=self.getSquarePiece(targetIndex)))
            targetIndex = index + 9
            targetPiece = self.getSquarePiece(targetIndex)
            if targetPiece.color == opponentcolor:
                moves.append(Move(index, targetIndex, flag=Flags.Capture, startPiece=self.getSquarePiece(index), targetPiece=self.getSquarePiece(targetIndex)))
        elif friendlycolor == Color.Black:
            forwardsquare = index - 8
            twosquare = index - 16
            forwardpiece = self.getSquarePiece(forwardsquare)
            if index < 8:
                return []
            if index in [48, 49, 50, 51, 52, 53, 54, 55]:
                targetSquare = twosquare
                targetPiece = self.getSquarePiece(targetSquare)
                if targetPiece.typ == Pieces.Empty and forwardpiece.typ == Pieces.Empty:
                    moves.append(Move(index, targetSquare, flag=Flags.PawnTwoMove, startPiece=self.getSquarePiece(index), targetPiece=self.getSquarePiece(targetSquare)))
            targetIndex = index - 9
            targetPiece = self.getSquarePiece(targetIndex)
            if targetPiece.color == opponentcolor:
                moves.append(Move(index, targetIndex, flag=Flags.Capture, startPiece=self.getSquarePiece(index), targetPiece=self.getSquarePiece(targetIndex)))
            targetIndex = index - 7
            targetPiece = self.getSquarePiece(targetIndex)
            if targetPiece.color == opponentcolor:
                moves.append(Move(index, targetIndex, flag=Flags.Capture, startPiece=self.getSquarePiece(index), targetPiece=self.getSquarePiece(targetIndex)))
        forwardpiece = self.getSquarePiece(forwardsquare)
        if forwardpiece.typ == Pieces.Empty:
            moves.append(Move(index, forwardsquare, startPiece=self.getSquarePiece(index), targetPiece=self.getSquarePiece(forwardsquare)))
        
        return moves
    def calcKingMoves(self, index : int):
        moves = []
        piece = self.getSquarePiece(index)
        friendlycolor = piece.color
        opponentcolor = piece.getEnemyColor()
        for i in Config.DIRECTIONOFFSETS:
            targetIndex = index + i
            if targetIndex > self.SquareCount-1:
                continue
            targetPiece = self.getSquarePiece(targetIndex)
            startPos = self.getCoordinatesByIndex(index)
            targetPos = self.getCoordinatesByIndex(targetIndex)
            difference = Vector2(abs(startPos.x - targetPos.x), abs(startPos.y - targetPos.y))
            if difference.x > 1 or difference.y > 1:
                continue
            if targetPiece.isColor(friendlycolor):
                print(targetIndex, targetPiece, friendlycolor, opponentcolor)
                continue
            if targetPiece.isColor(opponentcolor):
                moves.append(Move(index, targetIndex,flag=Flags.Capture, startPiece=self.getSquarePiece(index), targetPiece=self.getSquarePiece(targetIndex)))
                continue
            moves.append(Move(index, targetIndex, startPiece=self.getSquarePiece(index), targetPiece=self.getSquarePiece(targetIndex)))
        return moves
    def calcSlidingMoves(self, index : int):
        moves = []
        piece = self.getSquarePiece(index)
        startIndex = 4 if piece.isType(Pieces.Bishop) else 0
        endIndex = 4 if piece.isType(Pieces.Rook) else 8
        friendlycolor = piece.color
        opponentcolor = piece.getEnemyColor()
        for dirIndex in range(startIndex, endIndex):
            for n in range(0, self.NumSquaresToEdge[index][dirIndex]):
                targetIndex = index + Config.DIRECTIONOFFSETS[dirIndex] * (n + 1)
                targetPiece = self.getSquarePiece(targetIndex)
                if targetPiece.isColor(friendlycolor):
                    break
                
                if targetPiece.isColor(opponentcolor):
                    moves.append(Move(index, targetIndex,flag=Flags.Capture, startPiece=self.getSquarePiece(index), targetPiece=self.getSquarePiece(targetIndex)))
                    break
                moves.append(Move(index, targetIndex, startPiece=self.getSquarePiece(index), targetPiece=self.getSquarePiece(targetIndex)))
        return moves
                
if __name__ == "__main__"        :
    b = Board()
    b.loadFEN()