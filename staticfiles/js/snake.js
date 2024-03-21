let CellWidth = 20;
const StartDirection = 1;
const StartLength = 1;
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");
const BackgroundColor = "#090909";
const Directions = [{x : 0, y : -1},{x : 1, y : 0}, {x : 0, y : 1}, {x : -1, y : 0}];
let PlayerDirection = StartDirection;
let Highscore = 0;
const Tile = {
    create : function(index, direction, x, y)
    {
        return {
            index : index,
            direction : direction,
            lastdirection : direction,
            x : x,
            y : y
        }
    }
}
const Food = {
    new : function(x,y)
    {
        return {
            x : x,
            y : y
        }
    }
}
var Snake = {
    init : function()
    {
        this.Tiles = [];
        this.paused = false;
        this.Food = [];
        this.spawnFood();
        this.addTile(0, StartDirection, Math.floor(Math.floor(canvas.width/CellWidth)/2), Math.floor(Math.floor(canvas.height/CellWidth)/2));
    },
    addTile : function(index, direction, x, y)
    {
        this.Tiles.push(Tile.create(index, direction, x, y));
    },
    addTail : function()
    {
        let dir = this.Tiles[this.Tiles.length-1].direction;
        let newdir = 0
        if(dir == 0)
        {
            newdir = 2;
        }else if(dir == 1)
        {
            newdir = 3;
        }else if(dir == 3)
        {
            newdir = 1;
        }
        x = this.Tiles[this.Tiles.length-1].x + Directions[newdir].x;
        y = this.Tiles[this.Tiles.length-1].y + Directions[newdir].y;
        this.addTile(this.Tiles.length, this.Tiles[this.Tiles.length-1].direction, x,y);
    },
    spawnFood : function()
    {
        let maxx = Math.floor(canvas.width/CellWidth)-1
        let maxy = Math.floor(canvas.height/CellWidth)-1
        let x = Math.floor(Math.random() * (maxx + 1))
        let y = Math.floor(Math.random() * (maxy + 1))
        while(this.snakeOnPos(x,y))
        {
            x = Math.floor(Math.random() * (maxx + 1))
            y = Math.floor(Math.random() * (maxy + 1))
        }
        this.Food.push(Food.new(x,y));
    },
    snakeOnPos : function(x,y, exceptIndex) 
    {
        for(let i = 0; i < this.Tiles.length; i++)
        {
            if(i == exceptIndex)
                continue;
            let tile = this.Tiles[i];
            if(tile.x == x && tile.y == y)
            {
                return true;
            }
        }
        return false;
    },
    physicsStep : function()
    {
        this.Tiles[0].direction = PlayerDirection;
        for(let i = 0; i < this.Tiles.length; i++)
        {
            this.Tiles[i].lastdirection = this.Tiles[i].direction;
        }
        for(let i = 0; i < this.Tiles.length; i++)
        {
            this.Tiles[i].x += Directions[this.Tiles[i].direction].x
            this.Tiles[i].y += Directions[this.Tiles[i].direction].y
            if(this.Tiles[i].x < 0)
            {
                this.Tiles[i].x = Math.floor(canvas.width/CellWidth)-1;
            }
            else if(this.Tiles[i].x > Math.floor(canvas.width/CellWidth)-1)
            {
                this.Tiles[i].x = 0;
            }
            if(this.Tiles[i].y < 0)
            {
                this.Tiles[i].y = Math.floor(canvas.height/CellWidth)-1;
            }
            else if(this.Tiles[i].y > Math.floor(canvas.height/CellWidth)-1)
            {
                this.Tiles[i].y = 0;
            }
            if(i > 0)
            {
                let lasttile = this.Tiles[i-1];
                this.Tiles[i].direction = lasttile.lastdirection;
            }
        }
        let collide = this.snakeOnPos(this.Tiles[0].x, this.Tiles[0].y, 0)
        if(collide)
        {
            this.paused = true;
        }
        for(let i = 0; i < this.Food.length; i++)
        {
            let food = this.Food[i];
            if(food.x == this.Tiles[0].x && food.y == this.Tiles[0].y)
            {
                this.Food.splice(i, 1);
                this.addTail();
                this.spawnFood();
            }
        }
    },
    showEndScreen : function()
    {
        console.log("draw");
        ctx.fillStyle = "#FFA500";
        let score = this.Tiles.length-1;
        if(score > Highscore)
            Highscore = score;
        ctx.font = "100px Arial";
        let width = ctx.measureText("Game Over").width;
        ctx.fillText("Game Over", canvas.width/2 - width/2, 200);
        ctx.font = "50px Arial";
        width = ctx.measureText("Score: " + score).width;
        let width2 = ctx.measureText("Highscore: " + Highscore).width;
        ctx.fillText("Score: " + score, canvas.width/2 - width/2, 250);
        ctx.fillText("Highscore: " + Highscore, canvas.width/2 - width2/2, 300);
        ctx.font = "30px Arial";
        width = ctx.measureText("Press any button to restart").width;
        ctx.fillText("Press any button to restart", canvas.width/2 - width/2, 400);
    },
    draw : function() {
        ctx.fillStyle = "#00FF00";
        for(let i = 0; i < this.Tiles.length; i++)
        {
            let tile = this.Tiles[i];
            ctx.fillRect(tile.x*CellWidth, tile.y*CellWidth, CellWidth+2, CellWidth+2);
        }
        ctx.fillStyle = "#964B00";
        for(let i = 0; i < this.Food.length; i++)
        {
            let food = this.Food[i];
            ctx.fillRect(food.x*CellWidth+3.5, food.y*CellWidth+3.5, CellWidth-5, CellWidth-5);
        }
    }
}
function drawBackground()
{
    ctx.clearRect(0,0,canvas.width, canvas.height);
    ctx.fillStyle = BackgroundColor;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#808080";
    let width = Math.floor(canvas.width-2/CellWidth);
    let height = Math.floor(canvas.height-2/CellWidth);
    for(let i = 0; i < width; i++)
    {
        ctx.fillRect(i*CellWidth, 0, 2, canvas.height);
    }   
    for(let i = 0; i < height; i++)
    {
        ctx.fillRect(0, i*CellWidth, canvas.width, 2);
    }
}
Game = Object.assign({}, Snake);
Game.init();
if(StartLength > 1)
{
    for(let i = 0; i < StartLength; i++)
    {
        Game.addTail();
    }
}
function loop()
{
    Game.physicsStep();
    drawBackground();
    Game.draw();
    if(!Game.paused)
    {
        setTimeout(loop, 100);
    }else{
        Game.showEndScreen();
    }
}
document.addEventListener("keydown", function(evt) {
    if(Game.paused)
    {
        console.log("redo");
        Game = Object.assign({}, Snake);
        Game.init();
        if(StartLength > 1)
        {
            for(let i = 0; i < StartLength; i++)
            {
                Game.addTail();
            }
        }
        loop();
    }
    if(evt.key == "ArrowUp" && Game.Tiles[0].direction != 2)
    {
        PlayerDirection = 0;
    }else if(evt.key == "ArrowRight" && Game.Tiles[0].direction != 3)
    {
        PlayerDirection = 1;
    }else if(evt.key == "ArrowDown" && Game.Tiles[0].direction != 0)
    {
        PlayerDirection = 2;
    }else if(evt.key == "ArrowLeft" && Game.Tiles[0].direction != 1)
    {
        PlayerDirection = 3;
    }
});
loop();