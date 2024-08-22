import Backend
import queue
import TelegramHandler as T

InterThreadQueue = queue.Queue()


TelegramObj = T.TelegramHandler(InterThreadQueue)
TelegramObj.run()