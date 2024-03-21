const Canvas = document.getElementById("gameCanvas")
const ctx = Canvas.getContext("2d")
const RoomName = document.getElementById('my-element').dataset.name;
let BoardFEN = document.getElementById('boardfen').dataset.name;
let Moves = document.getElementById('moves').dataset.name;
const PlayerColor = parseInt(document.getElementById('color').dataset.name);
Moves = JSON.parse(Moves);
console.log(Moves);
let url = 'ws://' + window.location.host + '/ws/chess/' + RoomName.toString() + '/';

let BoardBlackColor = "#964B00";
let BoardWhiteColor = "#FFFFFF";

const Pieces = {
  Empty: 0,
  Pawn: 1,
  Bishop: 2,
  Knight: 3,
  Rook: 4,
  Queen: 5,
  King: 6,
}

const FenChars = [
  0,
  "p",
  "b",
  "n",
  "r",
  "q",
  "k",
]

const PieceFENs = {
  "p": Pieces.Pawn,
  "b": Pieces.Bishop,
  "n": Pieces.Knight,
  "r": Pieces.Rook,
  "q": Pieces.Queen,
  "k": Pieces.King,
}


const Colors = {
  None: 0,
  White: 1,
  Black: 2,
}

var Square = {
  new: function(index, piece, color)
  {
    return{
      index: index,
      piece: piece,
      color: color,
    }
  }
}

let Squares = []
for(var i = 0; i < 64; i++)
{
  Squares.push(Square.new(i, Pieces.None, Colors.None));
}

var Vector2 = {
	new: function (x, y) {
		return {
			x : x,
      y : y
		};
	}
};
let CanvasSize = Vector2.new(Canvas.width, Canvas.height);
let TileSize = Vector2.new(CanvasSize.x/8, CanvasSize.y/8);
 

const BlackQueenIm = new Image(TileSize.x, TileSize.y);
const BlackBishopIm = new Image(TileSize.x, TileSize.y);
const BlackKnightIm = new Image(TileSize.x, TileSize.y);
const BlackKingIm = new Image(TileSize.x, TileSize.y);
const BlackRookIm = new Image(TileSize.x, TileSize.y);
const BlackPawnIm = new Image(TileSize.x, TileSize.y);
const WhiteKingIm = new Image(TileSize.x, TileSize.y);
const WhiteQueenIm = new Image(TileSize.x, TileSize.y);
const WhiteBishopIm = new Image(TileSize.x, TileSize.y);
const WhiteKnightIm = new Image(TileSize.x, TileSize.y);
const WhiteRookIm = new Image(TileSize.x, TileSize.y);
const WhitePawnIm = new Image(TileSize.x, TileSize.y);
BlackKingIm.src = BlackKingUrl
BlackQueenIm.src = BlackQueenUrl
BlackBishopIm.src = BlackBishopUrl
BlackKnightIm.src = BlackKnightUrl
BlackRookIm.src = BlackRookUrl
BlackPawnIm.src = BlackPawnUrl
WhiteKingIm.src = WhiteKingUrl
WhiteQueenIm.src = WhiteQueenUrl
WhiteBishopIm.src = WhiteBishopUrl
WhiteKnightIm.src = WhiteKnightUrl
WhiteRookIm.src = WhiteRookUrl
WhitePawnIm.src = WhitePawnUrl


const Images = [
  [],
  [WhitePawnIm, BlackPawnIm],
  [WhiteBishopIm, BlackBishopIm],
  [WhiteKnightIm, BlackKnightIm],
  [WhiteRookIm, BlackRookIm],
  [WhiteQueenIm, BlackQueenIm],
  [WhiteKingIm, BlackKingIm],
]



let HoldingStartSquare = -1
let HoldingPeace = Pieces.None
let mousePos = Vector2.new(0,0)
let mousep = Vector2.new(0,0)

const socket = new WebSocket(url);
console.log(url);

function posToIndex(pos)
{
  var y = Math.floor(pos.y/TileSize.y)
  var x = Math.floor(pos.x/TileSize.x)
  var index = x + y*8;
  return index;
}

function getMousePos(canvas, evt, coordinatesystem) {
  var rect = canvas.getBoundingClientRect();
  if(coordinatesystem)
  {
    return {
      x: evt.clientX - rect.left,
      y: evt.clientY - rect.top
  };
  }else{
    return {
        x: evt.clientX - rect.left,
        y: Math.abs(evt.clientY - rect.top - rect.height)
    };
  }
}


Canvas.addEventListener("mousedown", function(evt){
  var index = posToIndex(mousep);
  if(Squares[index].piece == Pieces.None || Squares[index].color != PlayerColor) return
  HoldingStartSquare = index;
  HoldingPeace = Squares[index].piece;
});

Canvas.addEventListener("mouseup", function(evt){
  if(HoldingStartSquare == -1) return;
  var index = posToIndex(mousep);
  if(HoldingStartSquare == index){
    HoldingStartSquare = -1;
    HoldingPeace = Pieces.None;
    return;
  } 
  var startSquare = HoldingStartSquare;
  var targetSquare = index;

  socket.send(JSON.stringify({
    "type" : "play",
    "startSquare" : startSquare,
    "targetSquare": targetSquare,
  }))
  HoldingStartSquare = -1;
  HoldingPeace = Pieces.None;
});

function loadFEN()
{
  for(var i = 0; i < Squares.length; i++)
  {
    Squares[i].piece = Pieces.None;
    Squares[i].color = Colors.None;
  }
  var i = 0
  for(var v = 0; v < BoardFEN.length; v++)
  {
    var char = BoardFEN.charAt(v);
    if(char == "/")
    {
      continue;
    }else if(!isNaN(char))
    {
      var num = parseInt(char);
      i += num;
      continue;
    }else{
      var y = Math.floor(i/8)
      var x = i - y*8
      var _y = 7-y
      var index = _y*8 + x
      var _piece = Pieces.None
      var color = Colors.None
      for(var k = 1; k < FenChars.length; k++)
      {
        var Fenchar = FenChars[k]
        if(Fenchar == char)
        {
          color = Colors.Black;
          _piece = PieceFENs[Fenchar]
        }else if(Fenchar.toUpperCase() == char)
        {
          color = Colors.White;
          _piece = PieceFENs[Fenchar]
        }
      }
      Squares[index].piece = _piece;
      Squares[index].color = color;
      i += 1
    }
  }
}
function drawHoldingPeace()
{
  if(HoldingStartSquare == -1) return
  var y = Math.floor(HoldingStartSquare/8)
  var x = HoldingStartSquare - y*8
  var _y = 7-y

  ctx.drawImage(Images[HoldingPeace][PlayerColor-1], mousep.x-TileSize.x/2, mousePos.y-TileSize.y/2, TileSize.x, TileSize.y)
}

function update() {
  CanvasSize = Vector2.new(Canvas.width, Canvas.height);
  TileSize = Vector2.new(CanvasSize.x/8, CanvasSize.y/8);
  var count = Vector2.new(Math.floor(CanvasSize.x/TileSize.x), Math.floor(CanvasSize.y/TileSize.y));
  ctx.clearRect(0,0, CanvasSize.x, CanvasSize.y);

  var col = true;
  var peaceMoves = []
  if(HoldingStartSquare != -1)
  {
    peaceMoves.push(HoldingStartSquare);
    for(var i = 0; i < Moves.length; i++)
    {
      move = Moves[i];
      if(move.startSquare == HoldingStartSquare)
      {
        peaceMoves.push(move.targetSquare)
      }
    }
  }
  for(var x = 0; x < count.x; x++)
  {

    for(var y = 0; y < count.y; y++)
    {
      var _y = 7-y
      var Index = x+_y*8
      if(peaceMoves.includes(Index))
      {
        if(Index == HoldingStartSquare)
        {
          ctx.fillStyle="#79b6c9"
        }else{
          if(col)
          {
            ctx.fillStyle="#FFFF00";
          }else{
            ctx.fillStyle="#C7AF59";
          }
        }
      }else
      {
        if(col)
        {
          ctx.fillStyle=BoardWhiteColor;
        }else{
          ctx.fillStyle=BoardBlackColor;
        }
      }
      ctx.fillRect(x*TileSize.x, y*TileSize.y, TileSize.x, TileSize.y);
      col = !col
    } 
    col = !col
  }
  for(var i = 0; i < Squares.length; i++)
  {
    var square = Squares[i];
    if(square.piece != Pieces.None)
    {
      var y = Math.floor(i/8);
      var x = i - y*8;
      var _y = 7-y;
      var index = y*8 + x
      if(HoldingStartSquare == index)
      {
        continue
      }
      ctx.drawImage(Images[square.piece][square.color-1], x*TileSize.x, _y*TileSize.y, TileSize.x, TileSize.y);
    }
    
  }
  drawHoldingPeace()
  //count_x = 
  
  setTimeout(update, 5);
}


Canvas.addEventListener("mousemove", function(evt){
  var mousepos = getMousePos(Canvas, evt, true);
  var _mousep = getMousePos(Canvas, evt, false);
  mousePos.x = mousepos.x;
  mousePos.y = mousepos.y;
  mousep.x = _mousep.x;
  mousep.y = _mousep.y;
  //drawHoldingPeace()
});


socket.onmessage = function(e) {
    text_data = JSON.parse(e.data);
    console.log(text_data);
    if(text_data["type"] == "play_move")
    {
      BoardFEN = text_data["board"]
      loadFEN()
      Moves = JSON.parse(text_data["new_moves"])
    }
}

socket.onerror = function(e) {
  console.log(e);
}

socket.onopen = function(e) {
  update()
    //console.log(e);
    //socket.send(JSON.stringify({"Test" : "Lol"}))
}

socket.onclose = function(e) {
  console.log(e);
}


loadFEN()