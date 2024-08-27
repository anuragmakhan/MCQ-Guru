import QuestionClass
import Type
import AppLogger as LOG
import db_setup
import appMain
import Timer

class TelegramSender():
    def __init__(self):
        self.app = appMain.appMain.get_instance()
        self.bot = self.app.Senderbot
        self.QuestionTimerMap = dict()
    
    def QueueHandler(self):
        while True:
            msg = self.app.TaskQueue.get_task()
            self.TimerEventHandler(msg)
            LOG.INF(f"QUEUE_HANDLER_RECEIVED_A_MESSAGE: TIMER_ID : {msg.timerId} EVENT {msg.event}")
    
    def TimerEventHandler(self,msg):
        LOG.INF(f"IN_TIMER_EVENT_HANDLER EVENT: {msg.event} TIMER_ID: {msg.timerId}")
        if(msg.event == Type.TimerEvent.QUIZ_TRIGGER_TIMER):
            self.triggerQuiz()
        elif (msg.event == Type.TimerEvent.QUIZ_QUESTION_TIMER):
            self.deleteQuestion(msg.timerId)
        else:
            LOG.INF(f"UNKNOWN_EVENT DROPPING")
    
    def deleteQuestion(self,timerID):
        if(self.QuestionTimerMap[timerID]):
            self.QuestionTimerMap[timerID].deleteQuestionFromChat()
            del self.QuestionTimerMap[timerID]
    
    def triggerQuiz(self):
        self.app.Timer.start_timer(Type.QUIZ_TRIGGER_TIMER_VAL,Type.TimerEvent.QUIZ_TRIGGER_TIMER)
        groups = db_setup.get_all_groups()
        if groups:
            response = "Registered Groups:\n"
            for group in groups:
                group_id, group_name, group_type = group
                response += f"ID: {group_id}, Name: {group_name}, Type: {group_type}\n"
                print(group)
                question = QuestionClass.Question(self.bot,group_id,IsDeleteRequired=True)
                if question.IsDeleteRequired == True:
                    print("success")
                    timer_id = self.app.Timer.start_timer(Type.QUIZ_QUESTION_TIMER_VAL,Type.TimerEvent.QUIZ_QUESTION_TIMER)
                    self.QuestionTimerMap[timer_id] = question
                else:
                    print("FAILED")
     