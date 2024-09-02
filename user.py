import QuestionClass
import Type
import time
import appMain
import AppLogger as LOG
import threading
import QuizClass

class UserState:
    IDLE = "IDLE"
    ATTENDING_QUIZ = "ATTENDING_QUIZ"
    BROWSING_CONTENT = "BROWSING_CONTENT"
    WAITING_FOR_RESPONSE = "WAITING_FOR_RESPONSE"
    COMPLETING_TASK = "COMPLETING_TASK"

class CurrentUser:
    def __init__(self, user_id):
        self.user_id = user_id
        self.app = appMain.appMain.get_instance()
        self.state = UserState.IDLE  # Additional state to track the user's activity
        self.activetimer = None #TimerId
        self.current_quiz_id = 0

    def trigger_quiz(self):
        quiz = QuizClass.Quiz(self.user_id)
        self.current_quiz_id = quiz.QuizId #QuizId Logic Need to corrected
        self.app.addQuiz(quiz.QuizId,quiz)
        QuizThread = threading.Thread(target=quiz.start_quiz)
        QuizThread.start()
        #user.CurrentUser(message.chat.id).start_quiz()
        
    def finish_quiz(self):
        self.app.getQuiz(self.current_quiz_id).finish_quiz()
        #quiz = QuizClass.Quiz(self.user_id)

    def set_state(self, new_state):
        self.state = new_state
        LOG.INF(f"User {self.user_id} state changed to: {new_state}")

    def get_state(self):
        return self.state
    
    def heartbeat(self):
        if self.activetimer == None:
            self.activetimer = self.app.Timer.start_timer(10,Type.TimerEvent.USER_HEARTBEAT)
        self.lastActive = time.time()
        LOG.INF(f"User {self.user_id} heartbeat received TIME: {self.lastActive}")
        

    def is_in_quiz(self):
        return self.is_attending_quiz
    

    def __str__(self):
        return f"User {self.user_id} ({self.username}): State - {self.state}"
