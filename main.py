import time
import TelegramHandler as T
import threading
import ThreadClass as TC
import queue
import Backend
import Type
import AppLogger as LOG
#TelegramBot = T.TelegramHandler()
#TelegramBot.start_bot()




        
#Creating a Multiple Thread
InterThreadQueue = queue.Queue()


#Telegram Handler Thread
TelegramObj = T.TelegramHandler(InterThreadQueue)
TelegramThread = threading.Thread(target=TelegramObj.run)
TelegramThread.start()

TelegramResponseThread = threading.Thread(target=TelegramObj.QueueHandler)
TelegramResponseThread.start()


#
BackendObj = Backend.Backend(InterThreadQueue)
BackendThread = threading.Thread(target=BackendObj.run)
BackendThread.start()

print("APPLICATION STARTED")
while True:
    task = InterThreadQueue.get()
    if task.receiver == Type.Modules.TELEGRAM:
        #TelegramObj.thread.add_task(task)
        LOG.INF("BACKEND_RESPONSE_DROPPED")
        print("TELEGRAM_MSG")
    elif task.receiver == Type.Modules.BACKEND:
        BackendObj.thread.add_task(task)
        print("BACKEND_MSG")
    elif task.receiver == Type.Modules.LOGGER:
        print("TO_LOGGER")
    else:
        print("UNKNOWN_MSG")
        time.sleep(2)

