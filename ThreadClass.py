import queue

class ThreadClass:
    def __init__(self, thread_id, name):
        self.thread_id = thread_id
        self.name = name
        self.queue = queue.Queue()

    def get_task(self):
        return self.queue.get()
    
    def add_task(self, task):
        self.queue.put(task)

    def stop(self):
        self.queue.put(None)
