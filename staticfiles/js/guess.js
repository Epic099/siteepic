let roomId = 0;
let url = 'ws://' + window.location.host + '/ws/guess/';

const GUESSDIGITS = 3;

let socket = new WebSocket(url);

function displayRoom() {
    document.getElementById("roomid").style.display = "none";
    document.getElementById("createR").style.display = "none";
    document.getElementById("joinR").style.display = "none";
    let disp = document.getElementById("roomDisplay");
    disp.style.display = "";
    disp.innerHTML = "Room ID: " + roomId;
    document.getElementById("number").style.display = "";
    document.getElementById("numok").style.display = "";
}

function startGuess()
{
    let numfield = document.getElementById("numfield");
    numfield.style.color = "transparent";
    numfield.style.caretColor = "#000000";
    numfield.style.backgroundColor = "#000000";
    numfield.value = "";
    document.getElementById("numok").style.display = "none";
    document.getElementById("guesscontainer").style.display = "";
    document.getElementById("guesshistory").style.display = "";
}

function createRoom() {
    data = {
        "type":"create"
    }
    socket.send(JSON.stringify(data));
}
function joinRoom() {
    id = document.getElementById("roomid").value;

    console.log("joining room (ID: " + id + ")");
    data = {
        "type":"join", "id" : id
    }
    socket.send(JSON.stringify(data));
}

function setNumber() {
    if(roomId == 0) {
        return;
    }
    var number = document.getElementById("numfield").value;
    if (number.length != GUESSDIGITS) { return }
    data = {
        "type":"setNumber", "id" : roomId, "data" : number
    };
    socket.send(JSON.stringify(data));
    startGuess();
}

function guess() {
    var val = document.getElementById("guessfield").value;
    data = {
        "type": "guess", "id" : roomId, "data" : val
    };
    socket.send(JSON.stringify(data));
}

function removeAllChildren(parent) {
    while (parent.firstChild) {
      parent.removeChild(parent.firstChild);
    }
  }

socket.onmessage = function(e) {
    var text_data = e.data;
    var data = JSON.parse(text_data);
    var typ = data["type"];
    if(typ == "create" || typ == "join") {
        var id = data["id"];
        roomId = id;
        displayRoom();
        document.getElementById("player1_name").innerHTML = data["player1"];
        if(typ == "join") {
            document.getElementById("player2_name").innerHTML = data["player2"];     
        }
    }else if(typ == "debug")
    {
        var text = data["text"];
        console.log("Server message: " + text);
    }else if(typ == "kick")
    {
        roomId = 0;
        var text = data["text"];
        console.log("Server message: " + text);
        console.log("Kicked from room")
        document.getElementById("roomid").style.display = "";
        document.getElementById("createR").style.display = "";
        document.getElementById("joinR").style.display = "";
        let disp = document.getElementById("roomDisplay");
        disp.style.display = "none";
        disp.innerHTML = "Room ID: " + roomId;
        document.getElementById("roomid").value = "";
        document.getElementById("number").style.display = "none";
    }else if(typ == "guess")
    {
        player = data["player"];
        number = data["guess"];
        result = data["result"];
        list = document.getElementById("player" + player + "_history");
        li = document.createElement("li");
        li.innerHTML = number + " | ";
        result.forEach(element => {
            if(element == 2)
            {
                li.innerHTML += "🟩"
            }else if(element == 1) {
                li.innerHTML += "🟨"
            }else {
                li.innerHTML += "⬛"
            }
        });
        list.appendChild(li);
        console.log("Player " + player + " guessed " + number + " with result " + result);
    }else if(typ == "join")
    {
        plr1 = data["player1"];
        plr2 = data["player2"];

        document.getElementById("player1_name").innerHTML = plr1;
        document.getElementById("player2_name").innerHTML = plr2;
    }else if(typ == "end") {
        console.log("Game ended \nPlayer " + data['winner'] + " won the game");
        document.getElementById("header").innerHTML = "Spieler " + data['winner_name'] +  " hat das Spiel gewonnen.";
        var win1  = document.getElementById("win1");
        var win2  = document.getElementById("win2");
        win1.innerHTML = document.getElementById("player1_name").innerHTML + " | " + data['number1'] 
        win2.innerHTML = document.getElementById("player2_name").innerHTML + " | " + data['number2']
        win1.style.display = "";
        win2.style.display = "";
        setTimeout(() => {
            roomId = 0;
            var text = data["text"];
            document.getElementById("roomid").style.display = "";
            document.getElementById("createR").style.display = "";
            document.getElementById("joinR").style.display = "";
            let disp = document.getElementById("roomDisplay");
            disp.style.display = "none";
            disp.innerHTML = "Room ID: " + roomId;
            document.getElementById("roomid").value = "";
            document.getElementById("number").style.display = "none";
            document.getElementById("numok").style.display = "none";
            document.getElementById("guesscontainer").style.display = "none";
            document.getElementById("guesshistory").style.display = "none";
            document.getElementById("number").style.display = "none";
            document.getElementById("guessfield").value = "";
            document.getElementById("header").innerHTML = "Number-Guess";
            let numfield = document.getElementById("numfield");
            numfield.style.color = "black";
            numfield.style.caretColor = "#FFFFFF";
            numfield.style.backgroundColor = "#FFFFFF";
            win1.innerHTML = ""
            win2.innerHTML = ""
            win1.style.display = "none";
            win2.style.display = "none";

            removeAllChildren(document.getElementById("player1_history"));
            removeAllChildren(document.getElementById("player2_history"));

            document.getElementById("player1_name").innerHTML = "Player 1";
            document.getElementById("player2_name").innerHTML = "Player 2";
        }, 5000);
    
    }
}
socket.onclose = function(e) {
    console.log("Connection closed");
    console.log(e);
}
socket.onopen = function(e) {
    console.log("Client connection established");
}
