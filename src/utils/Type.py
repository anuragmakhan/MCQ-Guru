from dataclasses import dataclass



QUIZ_QUESTION_TIMER_VAL = 60*60 #seconds
QUIZ_TRIGGER_TIMER_VAL = 75*60

class TimerEvent:
    QUIZ_QUESTION_TIMER = 1
    QUIZ_TRIGGER_TIMER = 2
    USER_HEARTBEAT = 3

class Modules:
    TELEGRAM = 1
    BACKEND = 2
    LOGGER = 3
    TELEGRAM_RESPONSE_QUEUE = 4

class UserStates:
    START = 1
    MOVIE_SEARCH = 2


class Timermsg:
    def __init__(self,timerId = None,event = None):
        self.timerId: timerId # type: ignore
        self.event: event # type: ignore
