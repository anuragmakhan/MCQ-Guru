

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
from src.utils import Type
import queue
from src.db import db_setup
from telebot.types import PollAnswer
from src.core import Timer
from src.core import user

from src.utils import AppLogger as LOG
#import SqlLite_Db_Connector as SQL
#import client
from src.core import TaskQueue


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
            self.QuestionDeleteTimerMap = dict()
            self.Timer = Timer.TimerManager()
            self.activeUser = dict()
            self.CurrentLiveQuiz = dict()
            self.pollIdQuizIDMap = dict()
    
    def getQuizIdByPollId(self,PollId):
        return  self.pollIdQuizIDMap.get(PollId)
    
    def addpollIdQuizIDMap(self,PollId,QuizId):
        self.pollIdQuizIDMap[PollId] = QuizId     
        
    def addQuiz(self,QuizId,QuizInstance):
        self.CurrentLiveQuiz[QuizId] = QuizInstance
        
    def getQuiz(self,QuizId):
        return self.CurrentLiveQuiz.get(QuizId)
        
    def addUser(self,userId):
        user_t = user.CurrentUser(userId)
        self.activeUser[userId] = user_t
        return user_t
        
    def getUser(self,userId):
        ret = self.activeUser.get(userId)
        if None == ret:
            return self.addUser(userId)
        return ret
    
    def dumpStats():
        pass

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = appMain()
        return cls._instance
        
