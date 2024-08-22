from dataclasses import dataclass

class TimerEvent:
    QUIZ_QUESTION_TIMER = 1
    QUIZ_TRIGGER_TIMER = 2

QUIZ_QUESTION_TIMER_VAL = 60*60 #seconds, 30 min 
QUIZ_TRIGGER_TIMER_VAL = 90*60

class Action:
    MOVIE_SEARCH = 1
    RESPONSE_TO_USER =2
    START_QUIZ_TIMER = 3

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

class Timermsg:
    def __init__(self,timerId = None,event = None,message = None):
        self.timerId: timerId
        self.event: event
class InterThreadMsg:
    def __init__(self, msg = None, sender = None, receiver = None):
        self.sender = sender
        self.receiver = receiver
        self.msg = msg
        