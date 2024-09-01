import threading
import TelegramSender

import TelegramReceiver
import InterThreadQueueHandler

TReceiver = TelegramReceiver.TelegramReceiver()

TelegramThread = threading.Thread(target=TReceiver.run)
TelegramThread.start()

TSender = TelegramSender.TelegramSender()
TSender.triggerQuiz()

InterThreadQueueHandler.InterThreadQueueHandler()


print("APPLICATION STARTED")

TelegramThread.join()
