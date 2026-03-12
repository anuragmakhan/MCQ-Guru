import time
import threading
import uuid
import asyncio
from src.utils import AppLogger as LOG
from src.utils import Type
from src.core import TaskQueue
from src import appMain

class TimerManager:
    def __init__(self):
        self.timers = {}
        self.app = appMain.appMain.get_instance()

    def start_timer(self,duration, event):
        # Generate a unique timer ID
        timer_id = str(uuid.uuid4())
        try:
            loop = asyncio.get_running_loop()
            self.timers[timer_id] = loop.create_task(self._run_timer(timer_id, duration, event))
        except RuntimeError:
            timer_thread = threading.Thread(target=lambda: asyncio.run(self._run_timer(timer_id, duration, event)), daemon=True)
            timer_thread.start()
            self.timers[timer_id] = timer_thread
        
        LOG.INF(f"Timer {timer_id} started for {duration} seconds.")
        return timer_id

    async def _run_timer(self, timer_id, duration, event):
        await asyncio.sleep(duration)
        self.On_timer_expiry(timer_id, event)
        #callback(event)
        # Remove the timer from the dictionary after it expires
        self.timers.pop(timer_id, None)
        
    def On_timer_expiry(self, timer_id, event):
        LOG.INF(f"TIMER_EXPIRED: TIMER_ID : {timer_id} EVENT {event}")
        msg = Type.Timermsg()
        msg.timerId = timer_id
        msg.event = event
        self.app.TaskQueue.add_task(msg)
        #TQue.add_task(msg)
