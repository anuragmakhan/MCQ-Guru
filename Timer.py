import time
import threading
import uuid

class TimerManager:
    def __init__(self):
        self.timers = {}

    def start_timer(self, duration, callback):
        # Generate a unique timer ID
        timer_id = str(uuid.uuid4())
        # Create and start a new thread for the timer
        timer_thread = threading.Thread(target=self._run_timer, args=(timer_id, duration, callback))
        timer_thread.start()
        # Store the timer information
        self.timers[timer_id] = timer_thread
        #print(f"Timer {timer_id} started for {duration} seconds.")
        return timer_id

    def _run_timer(self, timer_id, duration, callback):
        time.sleep(duration)
        callback(timer_id)
        # Remove the timer from the dictionary after it expires
        self.timers.pop(timer_id, None)
        #print(f"Timer {timer_id} expired and callback executed.")

# Example callback function
def timer_expiry(timer_id):
    print(f"Timer {timer_id} has expired!")

# Example usage
timer_manager = TimerManager()
print("STARTING All thread")
for x in range(100000):
    timer_id = timer_manager.start_timer(100, timer_expiry)  # Timer for 5 seconds

print("All thread started")
