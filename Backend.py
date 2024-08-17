import Type
import ThreadClass
import AppLogger as LOG

# Define the events that can trigger state transitions
class Events:
    START_BUTTON_PRESSED = 1
    STOP_BUTTON_PRESSED = 2
    PAUSE_BUTTON_PRESSED = 3
    RESUME_BUTTON_PRESSED = 4

# Define the FSM class
class User:
    def __init__(self):
        self.current_state = Type.UserStates.START
        self.UserID = ""
        
    def changeUserState(self,NewState):
        self.current_state = NewState

class Backend:
    def __init__(self,Que):
        self.thread_id = Type.Modules.BACKEND
        self.commonQueue = Que
        self.UserMap = {}
        self.name = "BACKEND THREAD"
        self.thread = ThreadClass.ThreadClass(self.thread_id, self.name)

    def getUser(self,UserId):
        if UserId in self.UserMap:
            return self.UserMap[UserId]
        else:
            self.UserMap[UserId] = User()
        
    def fsmHandler(self,msg):
        # FSM handler for backend thread
        #LOG.INF("LOG_FROM_FSM "+ task.msg.userId,task.msg.action,task.msg.message)
        msg.message = "RESPONSE_FROM_BACKEND"
        msg.action = Type.Action.RESPONSE_TO_USER
        self.write_to_common_queue(msg)
        
        
    def run(self):
        LOG.INF("THREAD ID: " + str(self.thread_id) + " NAME: " + self.name + " STARTED")
        #print(f"Thread {self.thread_id} ({self.name}) started")
        while True:
            task = self.thread.get_task()
            self.fsmHandler(task.msg)
        print(f"Thread {self.thread_id} ({self.name}) exiting")
        
    def write_to_common_queue(self,msg):
        interMsg = Type.InterThreadMsg()
        interMsg.msg = msg
        interMsg.sender = Type.Modules.BACKEND
        interMsg.receiver = Type.Modules.TELEGRAM
        LOG.INF("MESSAGE_SENT_TO_COMMON_QUEUE_FROM_BACKEND USER_ID: "+ msg.userId)
        self.commonQueue.put(interMsg)
        return