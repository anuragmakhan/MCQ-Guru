
import db_setup
import AppLogger as LOG
import Type
import Timer
import appMain

class Question:
    def __init__(self,chatId,IsDeleteRequired = False):
        self.app = appMain.appMain.get_instance()
        self.question = db_setup.get_random_question()
        self.question_text = self.question[3]
        self.options = [self.question[4], self.question[5], self.question[6], self.question[7]]
        self.correct_option = self.question[8]
        self.chatId = chatId
        self.pollId = None
        self.message_id = None
        self.correct_option_id = self.get_correct_option_id()
        self.IsDeleteRequired = IsDeleteRequired
        self.bot = self.app.Senderbot
        self.sendQuestion()
        #Timer.TimerManager.start_timer(Type.QUIZ_QUESTION_TIMER_VAL,self.deleteQuestionFromChat)
        
    def deleteQuestionFromChat(self):
        if self.IsDeleteRequired == True:
            self.bot.delete_message(chat_id=self.chatId, message_id=self.message_id)
            LOG.INF(f"GROUP_ID {self.chatId} QUIZ_ID {self.pollId} DELETED")
    
    def get_correct_option_id(self):
        for i in range(len(self.options)):
            if self.options[i] == self.correct_option:
                return i
    def sendQuestion(self):
        try:
            poll_message = self.bot.send_poll(
                chat_id=self.chatId,
                question=self.question_text,
                options=self.options,
                is_anonymous=False,
                type="quiz",
                correct_option_id=self.correct_option_id# Set to False if you want to know who voted what
                )
            LOG.INF(f"CHAT_ID {self.chatId} QUIZ_ID {poll_message.poll.id} in poll {self.question_text} CORRECT OPTION ID : {self.correct_option_id}")
            #self.pollId = poll_message.poll.id
            self.message_id = poll_message.message_id
            self.pollId = poll_message.poll.id
            self.IsDeleteRequired = True
        except Exception as e:
            LOG.ERR(f"GROUP {self.chatId} QUIZ SEND FAILED Error: {str(e)}")
            self.IsDeleteRequired = False