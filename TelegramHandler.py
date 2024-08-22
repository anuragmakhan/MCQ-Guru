
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
import ThreadClass


class TelegramHandler:
    def __init__(self,Que):
        #self.bot = AsyncTeleBot(config.TELEGRAM_BOT_TOKEN)
        
        self.Senderbot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)
        self.bot = AsyncTeleBot(config.TELEGRAM_BOT_TOKEN)
        #self.db = SQL.DbConnector()
        self.msg_token_id = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.commonQueue = Que
        self.thread_id = Type.Modules.TELEGRAM_RESPONSE_QUEUE
        self.name = "TELEGRAM_RESPONSE_QUEUE"
        self.thread = ThreadClass.ThreadClass(self.thread_id, self.name)
        #self.Client = client.camp_client()
        #self._start_thread(self._backend_response, "client_request_handler")
        self.Timer = Timer.TimerManager()
        self.QuestionTimerMap = dict()
        self.triggerQuiz()

        @self.bot.callback_query_handler(func=lambda call: True)
        async def callback_handler(call):
            pass

        @self.bot.message_handler(func=lambda message: True)
        async def echo_message(message):
            #print("ALL OK")
            chat_id = message.chat.id
            chat_type = message.chat.type
            if chat_type == 'group' or chat_type == 'supergroup':
                if db_setup.get_group(chat_id):
                    LOG.INF("EXISTING_USER_GROUP: ID: " + str(chat_id))
                else:
                    group_name = message.chat.title
                    # Register the group in the database
                    db_setup.add_group(chat_id, group_name, chat_type)
                    LOG.INF("NEW_GROUP_REGISTERED: ID: " + str(chat_id))
                    #await self.bot.send_message(chat_id, f"Group '{group_name}' has been registered! Use /quiz to start a quiz.")

            user_id =  str(message.from_user.id)
            if db_setup.get_user(user_id):
                LOG.INF("EXISTING_USER: " + str(user_id))
            else:
                user_id = message.from_user.id
                username = message.from_user.username
                first_name = message.from_user.first_name
                last_name = message.from_user.last_name
                # Register the user in the database
                db_setup.add_user(user_id, username, first_name, last_name)
                LOG.INF("NEW_USER_REGISTERED: " + str(user_id))
            LOG.INF("CHAT_LOG USER_ID: " + str(user_id) + " Query: " + message.text)
            #LOG.INF("CHAT ID " + str(message.chat.id))
            self.write_to_common_queue(message.text,user_id,Type.Action.MOVIE_SEARCH)

        # Update listener to handle poll answers
        @self.bot.poll_answer_handler()
        async def handle_poll_answer(poll_answer):
            user_id = poll_answer.user.id
            poll_id = poll_answer.poll_id
            selected_option = poll_answer.option_ids[0]

            # Store user's response
            LOG.INF(f"User {user_id} selected option {selected_option} in poll {poll_id}")

            #print(f"User {user_id} selected option {selected_option} in poll {poll_id}")

    def triggerQuiz(self):
        self.Timer.start_timer(Type.QUIZ_TRIGGER_TIMER_VAL,Type.TimerEvent.QUIZ_TRIGGER_TIMER, self.thread)
        groups = db_setup.get_all_groups()
        question = db_setup.get_random_question()
        if groups:
            response = "Registered Groups:\n"
            for group in groups:
                group_id, group_name, group_type = group
                response += f"ID: {group_id}, Name: {group_name}, Type: {group_type}\n"
                print(group)
                
                
                self.Groupquiz(group_id,question)
        
    async def timer_expiry(self, timer_id,event):
        LOG.INF(f"TIMER_EXPIRED: TIMER_ID : {timer_id} EVENT {event}")
        if(event == Type.TimerEvent.QUIZ_QUESTION_TIMER):
            if(self.QuestionTimerMap[timer_id]):
                val =self.QuestionTimerMap[timer_id]
                del self.QuestionTimerMap[timer_id]
                #.write_to_common_queue("Quiz Time's Up!",self.QuestionTimerMap[timer_id],
                await self.bot.delete_message(chat_id=val[0], message_id=val[1])
                LOG.INF(f"GROUP_ID {val[0]} QUIZ_ID {val[1]} DELETED")
        
    def QueueHandler(self):
        LOG.INF("THREAD ID: " + str(self.thread_id) + " NAME: " + self.name + " STARTED")
        #print(f"Thread {self.thread_id} ({self.name}) started")
        
        while True:
            msg = self.thread.get_task()
            print("SENDING RESPONSE")
            LOG.INF(f"QUEUE_HANDLER_RECEIVED_A_MESSAGE: TIMER_ID : {msg.timerId} EVENT {msg.event}")
            if(msg.event == Type.TimerEvent.QUIZ_TRIGGER_TIMER):
                self.triggerQuiz()
            if (msg.event == Type.TimerEvent.QUIZ_QUESTION_TIMER):
                if(self.QuestionTimerMap[msg.timerId]):
                    val =self.QuestionTimerMap[msg.timerId]
                    #print(vl)
                    del self.QuestionTimerMap[msg.timerId]
                    #.write_to_common_queue("Quiz Time's Up!",self.QuestionTimerMap[timer_id],
                    self.Senderbot.delete_message(chat_id=val[0], message_id=val[1])
                    LOG.INF(f"GROUP_ID {val[0]} QUIZ_ID {val[1]} DELETED")
                
            #self.sendResponse(task.msg)
        print(f"Thread {self.thread_id} ({self.name}) exiting")
    
    def sendResponse(self,message):
        bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)
        bot.send_message(message.userId, text=message.message)
        
    def Groupquiz(self,groupId,question):
        if question:
            question_text = question[1]
            options = [question[2], question[3], question[4], question[5]]
            correct_option = question[6]
            
            try:
                poll_message = self.Senderbot.send_poll(
                    chat_id=groupId,
                    question=question_text,
                        options=options,
                        is_anonymous=False,
                        type="quiz"
                        correct_option_id=1# Set to False if you want to know who voted what
                )
                LOG.INF(f"GROUP_ID {groupId} QUIZ_ID {poll_message.poll.id} in poll {question_text}")
                timer_id = self.Timer.start_timer(Type.QUIZ_QUESTION_TIMER_VAL,Type.TimerEvent.QUIZ_QUESTION_TIMER,self.thread)

                # Delete the poll message after the timer expires
                self.QuestionTimerMap[timer_id] = [groupId,poll_message.message_id]
            except Exception as e:
                LOG.ERR(f"GROUP {groupId} QUIZ SEND FAILED Error: {str(e)}")

            
            
            # Wait for the specified timer duration
            

            #await self.bot.delete_message(chat_id=groupId, message_id=poll_message.message_id)

            # Optionally, you can send a message indicating that the quiz time has expired
            #await self.bot.send_message(chat_id=groupId, text="Time's up! The quiz has ended.")
                # Store the poll message ID to track responses
        
    def write_to_common_queue(self,message,UserId,action):
        msg = Type.msg()
        msg.action = action
        msg.message = message
        msg.userId = str(UserId)
        
        interMsg = Type.InterThreadMsg()
        
        interMsg.msg = msg
        interMsg.sender = Type.Modules.TELEGRAM
        interMsg.receiver = Type.Modules.BACKEND
        
        LOG.INF("MESSAGE_SENT_TO_COMMON_QUEUE_FROM_TELEGRAM USER_ID: "+ msg.userId)
        self.commonQueue.put(interMsg)
        return
        
        
    def run(self):
        # Add the update listener
        #self.bot.add_update_listener(self.handle_poll_answer)
        LOG.INF("THREAD ID: " + str(Type.Modules.TELEGRAM) + " NAME: TELEGRAM_LISTENER " + " STARTED")
        asyncio.run(self.bot.polling())
        print("TELEGRAM_LISTENER_THREAD_EXITED !!!!FATAL")