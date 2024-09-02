import uuid
import QuestionClass
import Type
import AppLogger as LOG
import appMain
from collections import defaultdict
from time import time, sleep


class Quiz:
    def __init__(self,user_id):
        self.QuizId = int(uuid.uuid4().int & (1<<64)-1)  # Convert to a 64-bit integer
        self.app = appMain.appMain.get_instance()
        self.user_id = user_id

        self.t = 10
        self.current_question_index = 0
        self.responses = defaultdict(list)  # Store responses keyed by user_id
        self.start_time = time()
        self.poll_ids = dict()  # Store poll IDs to track responses
        self.results = {}
        self.current_quiz_id = 7
    
    def start_quiz(self):
        if self.current_quiz_id != 0:
            question = QuestionClass.Question(self.user_id,IsDeleteRequired=True)
            self.app.addpollIdQuizIDMap(question.pollId,self.QuizId)
            self.poll_ids[question.pollId] = question
            if question.IsDeleteRequired == True:
                timer_id = self.app.Timer.start_timer(12,Type.TimerEvent.QUIZ_QUESTION_TIMER)
                self.app.QuestionDeleteTimerMap[timer_id] = question
            sleep(10)
            self.start_quiz()
        else:
            LOG.INF(f"QUIZ ENDED USER_ID {self.user_id}")
            #self.state = UserState.IDLE  # Additional state to track the user's activity

    async def handle_poll_answer(self, poll_answer):
        """
        Handle the user's response to a poll.
        
        Parameters:
        - poll_answer: The poll answer object from the Telegram API.
        """
        poll_id = poll_answer.poll_id
        user_id = poll_answer.user.id
        selected_option_index = poll_answer.option_ids[0]  # Assuming single choice

        question = self.poll_ids.get(poll_id)
        
        if question.correct_option_id == selected_option_index:
            self.responses[user_id].append(1)
        else:
            self.responses[user_id].append(0)   

    def calculate_results(self):
        """
        Calculate results for each user based on their responses.
        """
        wronganswer = 0
        correctanswer = 0
        for user_id, answers in self.responses.items():
            for x in answers:
                if x == 0:
                    wronganswer = wronganswer + 1
                elif x == 1:
                    correctanswer = correctanswer + 1
                    
            self.results[user_id] = {
                'userId': user_id,
                'score': correctanswer,
                'Wrong': wronganswer,
                'total': len(self.poll_ids),
                'percentage': (correctanswer / len(self.poll_ids)) * 100
            }
            
            print(self.results[user_id])

    def finish_quiz(self):
        self.is_attending_quiz = False
        self.calculate_results()
        LOG.INF(f"User {self.user_id} finished quiz {self.current_quiz_id}")
        self.current_quiz_id = 0
        self.state = "Idle"
