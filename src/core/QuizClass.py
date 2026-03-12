import uuid
from src.core import QuestionClass
from src.utils import Type
from src.utils import AppLogger as LOG
from src import appMain
from collections import defaultdict
from time import time
import asyncio
from src.db import db_setup

class Quiz:
    def __init__(self,user_id, subject = None):
        self.QuizId = int(uuid.uuid4().int & (1<<64)-1)  # Convert to a 64-bit integer
        self.app = appMain.appMain.get_instance()
        self.user_id = user_id
        self.subject = subject

        self.t = 10
        self.ToatlQuestionInQuiz = 10
        self.posted_question_count = 0
        self.responses = defaultdict(list)  # Store responses keyed by user_id
        self.start_time = time()
        self.poll_ids = dict()  # Store poll IDs to track responses
        self.results = {}
        self.current_quiz_id = 7
    
    async def start_quiz(self):
        if self.current_quiz_id != 0 and self.posted_question_count < self.ToatlQuestionInQuiz:
            question = QuestionClass.Question(self.user_id,IsDeleteRequired=True, subject=self.subject)
            self.app.addpollIdQuizIDMap(question.pollId,self.QuizId)
            self.poll_ids[question.pollId] = question
            if question.IsDeleteRequired == True:
                timer_id = self.app.Timer.start_timer(12,Type.TimerEvent.QUIZ_QUESTION_TIMER)
                self.app.QuestionDeleteTimerMap[timer_id] = question
            await asyncio.sleep(10)
            self.posted_question_count+=1
            await self.start_quiz()
        else:
            LOG.INF(f"QUIZ ENDED USER_ID {self.user_id}")
            self.finish_quiz()
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
        
        msg = "<b>📊 Quiz Report Card</b>\n\n"
        msg += "<b>Name       | Score</b>\n"
        msg += "<b>-------------------------------------------</b>\n"


        for user_id, answers in self.responses.items():
            for x in answers:
                if x == 0:
                    wronganswer = wronganswer + 1
                elif x == 1:
                    correctanswer = correctanswer + 1
                    
            self.results[user_id] = {
                'userName': db_setup.get_username_from_user_id(user_id),
                'score': correctanswer,
                'Wrong': wronganswer,
                'total': len(self.poll_ids),
                'Total SCORE': (correctanswer * 4 -  wronganswer*1)
            }
            # Add row for each person
            msg += f"{db_setup.get_username_from_user_id(user_id)}|{'      ' + str(correctanswer * 4 - wronganswer * 1)}\n"


        #LOG.INF(f"{db_setup.get_username_from_user_id(user_id)} {self.results[user_id]}")

    def finish_quiz(self):
        self.is_attending_quiz = False
        self.calculate_results()
        LOG.INF(f"User {self.user_id} finished quiz {self.current_quiz_id}")
        self.current_quiz_id = 0
        self.state = "Idle"
