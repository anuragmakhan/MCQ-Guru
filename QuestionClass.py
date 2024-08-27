
import db_setup
import AppLogger as LOG
import Type
import Timer
import appMain

class Question:
    def __init__(self,bot,chatId,IsDeleteRequired = False):
        self.app = appMain.appMain.get_instance()
        self.question = db_setup.get_random_question()
        self.question_text = self.question[1]
        self.options = [self.question[2], self.question[3], self.question[4], self.question[5]]
        self.correct_option = 1#self.question[6]
        self.chatId = chatId
        self.pollId = None
        self.IsDeleteRequired = IsDeleteRequired
        self.bot = bot
        self.sendQuestion()
        #Timer.TimerManager.start_timer(Type.QUIZ_QUESTION_TIMER_VAL,self.deleteQuestionFromChat)
        
    def deleteQuestionFromChat(self):
        if self.IsDeleteRequired == True:
            self.bot.delete_message(chat_id=self.chatId, message_id=self.pollId)
            LOG.INF(f"GROUP_ID {self.chatId} QUIZ_ID {self.pollId} DELETED")
    
    def sendQuestion(self):
        try:
            poll_message = self.bot.send_poll(
                chat_id=self.chatId,
                question=self.question_text,
                options=self.options,
                is_anonymous=False,
                type="quiz",
                correct_option_id=self.correct_option# Set to False if you want to know who voted what
                )
            LOG.INF(f"CHAT_ID {self.chatId} QUIZ_ID {poll_message.poll.id} in poll {self.question_text}")
            #self.pollId = poll_message.poll.id
            self.pollId = poll_message.message_id
            self.IsDeleteRequired = True
        except Exception as e:
            LOG.ERR(f"GROUP {self.chatId} QUIZ SEND FAILED Error: {str(e)}")
            self.IsDeleteRequired = False