import os, random
from . import models
import string
def randomId(length : int) :
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits

    all_chars = lowercase_letters + uppercase_letters + digits
    random_string = ''.join(random.sample(all_chars, length))
    return random_string    

def createRoom(length : int) -> models.GuessRoom: 
    id = randomId(length)
    while models.GuessRoom.objects.filter(roomId=id).count() > 0:
        id = randomId(length)
    room = models.GuessRoom.objects.create(roomId=id) 
    room.save()
    return room

def guess(number, guessNumber):
    num1 = str(number)
    num2 = str(guessNumber)
    result = []
    exclude = []
    counts = {"0" : 0, "1" : 0, "2" : 0, "3" : 0, "4" : 0, "5" : 0, "6" : 0, "7" : 0, "8" : 0, "9" : 0}
    for i in range(len(num1)):
        if num1[i] == num2[i]:
            result.append(2)
            exclude.append(i)
            counts[num2[i]] += 1
    for i in range(len(num1)):
        if i in exclude: continue
        if num1.count(num2[i]) > counts[num2[i]]:
            result.append(1)
            counts[num2[i]] += 1
    while len(result) < len(num1):
        result.append(0)
    return result


            
    
    