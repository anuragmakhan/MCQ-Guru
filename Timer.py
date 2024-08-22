import time
import threading
import uuid
import AppLogger as LOG
import Type
import ThreadClass

class TimerManager:
    def __init__(self):
        self.timers = {}
        self.thread_id = Type.Modules.TELEGRAM_RESPONSE_QUEUE
        self.name = "TIMER_QUEUE"
        self.thread = ThreadClass.ThreadClass(self.thread_id, self.name)

    def start_timer(self,duration, event, TQue):
        # Generate a unique timer ID
        timer_id = str(uuid.uuid4())
        # Create and start a new thread for the timer
        timer_thread = threading.Thread(target=self._run_timer, args=(timer_id, duration, event, TQue))
        timer_thread.start()
        # Store the timer information
        self.timers[timer_id] = timer_thread
        LOG.INF(f"Timer {timer_id} started for {duration} seconds.")
        return timer_id

    def _run_timer(self, timer_id, duration, event, TQue):
        time.sleep(duration)
        self.On_timer_expiry(timer_id, event, TQue)
        #callback(event)
        # Remove the timer from the dictionary after it expires
        self.timers.pop(timer_id, None)
        
    def On_timer_expiry(self, timer_id, event, TQue):
        LOG.INF(f"TIMER_EXPIRED: TIMER_ID : {timer_id} EVENT {event}")
        print(f"Timer {timer_id} has expired!")
        msg = Type.Timermsg()
        msg.timerId = timer_id
        msg.event = event
        TQue.add_task(msg)
