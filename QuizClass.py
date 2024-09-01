import uuid
import QuestionClass
import Type
import AppLogger as LOG
import time
import appMain


class Quiz:
    def __init__(self,user_id):
        self.QuizId = int(uuid.uuid4().int & (1<<64)-1)  # Convert to a 64-bit integer
        self.app = appMain.appMain.get_instance()
        self.user_id = user_id

        print(self.QuizId )
    
    def start_quiz(self):
        if self.current_quiz_id != 0:
            question = QuestionClass.Question(self.user_id,IsDeleteRequired=True)
            if question.IsDeleteRequired == True:
                print("success")
                timer_id = self.app.Timer.start_timer(12,Type.TimerEvent.QUIZ_QUESTION_TIMER)
                self.app.QuestionDeleteTimerMap[timer_id] = question
            else:
                print("FAILED")
            time.sleep(10)
            self.start_quiz()
        else:
            LOG.INF(f"QUIZ ENDED USER_ID {self.user_id}")
            #self.state = UserState.IDLE  # Additional state to track the user's activity
                

    def finish_quiz(self):
        self.is_attending_quiz = False
        LOG.INF(f"User {self.user_id} finished quiz {self.current_quiz_id}")
        self.current_quiz_id = 0
        self.state = "Idle"
