

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


class appMain:
    _instance = None  # Class variable to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(appMain, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):  # Prevent re-initialization
            self.initialized = True
            self.Senderbot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)
            self.ReceiverBot = AsyncTeleBot(config.TELEGRAM_BOT_TOKEN)
            self.TaskQueue = TaskQueue.TaskQueue()
            self.Timer = Timer.TimerManager()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = appMain()
        return cls._instance
        
