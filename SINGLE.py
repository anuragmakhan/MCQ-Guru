import telebot
import config
def sendResponse():
    bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)
    bot.send_message(6838148174, text="Hi,  Give me Admin Permission In your Group, then only i will be able to post Quiz")

sendResponse()