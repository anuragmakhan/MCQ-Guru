import AppLogger as LOG
import appMain
import Type
import threading

# Define the FSM class
class InterThreadQueueHandler:
    def __init__(self):
        self.app = appMain.appMain.get_instance()
        QueueHandler = threading.Thread(target=self.run)
        QueueHandler.start()

    def run(self):
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
        if(self.app.QuestionDeleteTimerMap[timerID]):
            self.app.QuestionDeleteTimerMap[timerID].deleteQuestionFromChat()
            del self.app.QuestionDeleteTimerMap[timerID]