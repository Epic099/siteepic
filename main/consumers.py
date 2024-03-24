import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from . import guess
from . import models

GUESSDIGITS = 3

def guessUser(id, user):
    room = models.GuessRoom.objects.get(roomId=id)
    if room.player1 == user:
        return 1
    elif room.player2 == user:
        return 2
    return False 
      
class GuessConsumer(WebsocketConsumer):
    def connect(self):
      self.room_name = "room"
      self.room_group_name = f'guess_{self.room_name}'
      async_to_sync(self.channel_layer.group_add)(
          self.room_group_name,
          self.channel_name
      )
      self.accept()
      
      self.send(text_data=json.dumps({
        'type' : "debug",
        'text' : 'Connection to Server established'
      }))
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        typ = text_data_json['type']
        if typ == "create":
            user = self.scope["user"]
            room = guess.createRoom(6)
            room.player1 = user
            room.save()
            id = room.roomId
            async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
            self.room_name = id
            self.room_group_name = f'guess_{self.room_name}'
            
            async_to_sync(self.channel_layer.group_add) (
                self.room_group_name,
                self.channel_name
            )
            
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'create',
                    'id':id,
                    'turn' : room.turn,
                    'player1' : room.player1.username,
                    'text': f"Connected to {id}"
                }
            )        
        elif typ == "join":
            id = None
            room = None
            try:
                id = text_data_json['id']
                room = models.GuessRoom.objects.get(roomId=id)
            except Exception as error:
                self.send(text_data=json.dumps({
                    'type' : "debug",
                    'text' : 'Login Failed, Room Id does not exist'
                }))
                return

            async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)
            self.room_name = id
            self.room_group_name = f'guess_{self.room_name}'
            room.player2 = self.scope["user"]
            room.save()
            
            async_to_sync(self.channel_layer.group_add) (
                self.room_group_name,
                self.channel_name
            )
            
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'join',
                    'id':id,
                    'turn' : room.turn,
                    'player1' : room.player1.username,
                    'player2' : room.player2.username,
                    'text': f"Connected to {id}"
                }
            )      
        elif typ == "setNumber":
            id = self.room_name
            user = self.scope["user"]
            number = text_data_json['data']
            room = models.GuessRoom.objects.get(roomId=id)
            if len(number) != GUESSDIGITS:
                self.send(text_data=json.dumps({
                    'type' : "debug",
                    'text' : f'Number invalid, must have {GUESSDIGITS} digits'
                }))
                return
            n = guessUser(id, user)
            if n == False: return 
            elif n == 1:
                room.number1 = number
            elif n == 2:
                room.number2 = number
            room.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'debug',
                    'id':id,
                    'text': f"Player {n} number successfully set"
                }
            )        
        elif typ == "guess":
            id = self.room_name
            result = []
            #try:
            num = text_data_json['data']
            user = self.scope["user"]
            room = models.GuessRoom.objects.get(roomId=id)
            if room.player1 == None or room.player2 == None or room.number1 == "" or room.number2 == "" or room.number1 == None or room.number2 == None:
                self.send(text_data=json.dumps({
                    'type' : "debug",
                    'text' : 'Guess Failed, Round has not started yet.'
                }))
                return
            player = guessUser(id, user)
            if player != room.turn:
                self.send(text_data=json.dumps({
                    'type' : "debug",
                    'text' : 'Guess Failed, its not your turn.'
                }))
                return
            number = ""
            if player == False: return
            elif player == 1:
                number = room.number2
            elif player == 2:
                number = room.number1
            result = guess.guess(number, num)
            room.turn = 1 if room.turn == 2 else 2
            room.save()
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'guess',
                    'id':id,
                    'player' : player,
                    'turn' : room.turn,
                    'guess' : num,
                    'result' : result,
                }
            )    
            if result.count(2) == len(result):
                name = room.player1.username if player == 1 else room.player2.username,
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type':'end',
                        'id' : id,
                        'winner' : player,
                        'winner_name' : name,
                        'number1' : room.number1,
                        'number2' : room.number2,
                        'text': f"Player {player} won the game",                        
                    }
                ) 
                room.delete()
           # except Exception as error:
            #    print(error)
    def create(self, event):
        id = event["id"]
        turn = event["turn"]
        text = event["text"]
        player1 = event["player1"]
        self.send(text_data=json.dumps({
            'type':'create',
            'id':id,
            'turn' : turn,
            'player1' : player1,
            'text': text
        }))
    def guess(self, event):
        id = event["id"]
        player = event["player"]
        guess = event["guess"]
        result = event["result"]
        self.send(text_data=json.dumps({
            'type':'guess',
            'id':id,
            'player' : player,
            'guess' : guess,
            'result' : result
        }))
    def join(self, event):
        id = event["id"]
        turn = event["turn"]
        text = event["text"]
        player1 = event["player1"]
        player2 = event["player2"]
        self.send(text_data=json.dumps({
            'type':'join',
            'id':id,
            'turn' : turn,
            'player1' : player1,
            'player2' : player2,
            'text': text
        }))
    def end(self, event):
        id = event["id"]
        winner = event["winner"]
        winner_name = event["winner_name"]
        number1 = event["number1"]
        number2 = event["number2"]
        text = event["text"]
        self.send(text_data=json.dumps({
            'type':'end',
            'id':id,
            'winner' : winner,
            'winner_name' : winner_name,
            'number1' : number1,
            'number2' : number2,
            'text': text
        }))
    def setNumber(self, event):
        id = event["id"]
    def debug(self, event):
        id = event["id"]
        text = event["text"]
        self.send(text_data=json.dumps({
            'type':'debug',
            'id':id,
            'text': text
        }))
    def kick(self, event):
        id = event["id"]
        text = event["text"]
        self.send(text_data=json.dumps({
            'type':'kick',
            'id':id,
            'text': text
        }))
    def disconnect(self, close_code):
        print(f'Connection closed: {close_code}')
        try:
            room = models.GuessRoom.objects.get(roomId=self.room_name)
            num = guessUser(self.room_name, self.scope["user"])
            if num == 2: 
                print("Player 2 has left the room")
                room.player2 = None
                room.save()
            elif num == 1:
                async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type':'kick',
                    'id':self.room_name,
                    'text': f"Host hast left the room"
                })        
                print("Host left the room, deleting room")
                room.delete()
        except Exception as error:
            print("User Disconnected without joining a room")
        async_to_sync(self.channel_layer.group_discard)(self.room_name, self.channel_name)