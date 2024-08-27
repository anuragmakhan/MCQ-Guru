import queue

class TaskQueue:
    def __init__(self):
        self.queue = queue.Queue()

    def get_task(self):
        return self.queue.get()
    
    def add_task(self, task):
        self.queue.put(task)

    def stop(self):
        self.queue.put(None)
