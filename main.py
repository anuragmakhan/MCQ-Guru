import threading
import TelegramSender

import TelegramReceiver

TReceiver = TelegramReceiver.TelegramReceiver()

TelegramThread = threading.Thread(target=TReceiver.run)
TelegramThread.start()

TSender = TelegramSender.TelegramSender()
TSender.triggerQuiz()
QueueHandler = threading.Thread(target=TSender.QueueHandler)
QueueHandler.start()


print("APPLICATION STARTED")

TelegramThread.join()
QueueHandler.join()
