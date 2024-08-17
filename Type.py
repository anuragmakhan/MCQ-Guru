from dataclasses import dataclass


class Action:
    MOVIE_SEARCH = 1
    RESPONSE_TO_USER =2

class Modules:
    TELEGRAM = 1
    BACKEND = 2
    LOGGER = 3
    TELEGRAM_RESPONSE_QUEUE = 4

class UserStates:
    START = 1
    MOVIE_SEARCH = 2

class msg:
    def __init__(self,userID = None,action = None,message = None):
        self.userId: userID
        self.action: action
        self.message: message
    
class InterThreadMsg:
    def __init__(self, msg = None, sender = None, receiver = None):
        self.sender = sender
        self.receiver = receiver
        self.msg = msg
        