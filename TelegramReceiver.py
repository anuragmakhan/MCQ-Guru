
import json
import threading
import time
import config
import asyncio
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from threading import Thread
from telebot.async_telebot import AsyncTeleBot
import telebot
import Type
import queue
import db_setup
from telebot.types import PollAnswer
import Timer

import AppLogger as LOG
#import SqlLite_Db_Connector as SQL
#import client
import TaskQueue
import appMain

class TelegramReceiver:
    def __init__(self):
        app = appMain.appMain.get_instance()
        self.bot = app.ReceiverBot

        @self.bot.message_handler(func=lambda message: True)
        async def echo_message(message):
            self.check_and_register_user(message)

        # Update listener to handle poll answers
        @self.bot.poll_answer_handler()
        async def handle_poll_answer(poll_answer):
            user_id = poll_answer.user.id
            poll_id = poll_answer.poll_id
            selected_option = poll_answer.option_ids[0]
            LOG.INF(f"User {user_id} selected option {selected_option} in poll {poll_id}")
        
    def run(self):
        asyncio.run(self.bot.polling())
        print("TELEGRAM_LISTENER_THREAD_EXITED !!!!FATAL")
    
    def check_and_register_user(self,message):
        chat_id = message.chat.id
        chat_type = message.chat.type
        LOG.INF(f"CHAT_LOG USER_ID: {message.from_user.id} CHAT_ID: {chat_id} CHAT_TYPE: {chat_type} TEXT: {message.text}")
        if chat_type == 'group' or chat_type == 'supergroup':
            if db_setup.get_group(chat_id):
                LOG.INF("EXISTING_USER_GROUP: ID: " + str(chat_id))
            else:
                db_setup.add_group(chat_id, message.chat.title, chat_type)
                LOG.INF("NEW_GROUP_REGISTERED: ID: " + str(chat_id))

        user_id =  str(message.from_user.id)
        if db_setup.get_user(user_id):
            LOG.INF("EXISTING_USER: " + str(user_id))
        else:
            db_setup.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
            LOG.INF("NEW_USER_REGISTERED: " + str(user_id))

