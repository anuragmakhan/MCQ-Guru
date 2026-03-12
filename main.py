import threading
from src.bot import TelegramSender

from src.bot import TelegramReceiver
from src.core import InterThreadQueueHandler

TReceiver = TelegramReceiver.TelegramReceiver()

TelegramThread = threading.Thread(target=TReceiver.run)
TelegramThread.start()

TSender = TelegramSender.TelegramSender()
TSender.triggerQuiz()

InterThreadQueueHandler.InterThreadQueueHandler()


from src.utils import AppLogger as LOG

LOG.INF("APPLICATION STARTED")

TelegramThread.join()
