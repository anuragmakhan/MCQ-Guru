import QuestionClass
import Type
import AppLogger as LOG
import db_setup
import appMain

class TelegramSender():
    def __init__(self):
        self.app = appMain.appMain.get_instance()
        self.bot = self.app.Senderbot
    
    
    
    #REQUIREMENT Trigger of GroupQuiz should be event based
    #After this change this file can be removed
    
    def triggerQuiz(self):
        self.app.Timer.start_timer(Type.QUIZ_TRIGGER_TIMER_VAL,Type.TimerEvent.QUIZ_TRIGGER_TIMER)
        groups = db_setup.get_all_groups()
        if groups:
            response = "Registered Groups:\n"
            for group in groups:
                group_id, group_name, group_type = group
                response += f"ID: {group_id}, Name: {group_name}, Type: {group_type}\n"
                print(group)
                question = QuestionClass.Question(group_id,IsDeleteRequired=True)
                if question.IsDeleteRequired == True:
                    timer_id = self.app.Timer.start_timer(Type.QUIZ_QUESTION_TIMER_VAL,Type.TimerEvent.QUIZ_QUESTION_TIMER)
                    self.app.QuestionDeleteTimerMap[timer_id] = question
     