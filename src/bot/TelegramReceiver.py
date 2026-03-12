import asyncio
from src.db import db_setup
from src.utils import AppLogger as LOG
from src import appMain
from src.core import user
import threading
import config
from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton

class TelegramReceiver:
    def __init__(self):
        self.app = appMain.appMain.get_instance()
        self.bot = self.app.ReceiverBot
        
        # Set commands
        asyncio.create_task(self.set_commands())

        # Handler for /start command
        @self.bot.message_handler(commands=['start'])
        async def send_welcome(message):
            await self.bot.send_message(message.chat.id, "Welcome to the bot! \n स्वागत है MCQguru में! 📚परीक्षा की तैयारी, ज्ञान बढ़ाने या खुद को चुनौती देने के लिए यह बॉट आपके लिए एक आदर्श साथी है।.\n To Start Quiz -> /startQuiz")
            # Optionally, check and register the user when they send the /start command
            self.check_and_register_user(message)
            
        @self.bot.message_handler(commands=['BackUpDb'])
        async def adminMsg(message):
            if str(message.from_user.id) != config.ADMIN_ID:
                await self.bot.send_message(message.chat.id, "Unauthorized. You are not an admin.")
                return
            db_setup.dump_db_t()
            LOG.INF("DB_BACKUP_DONE")
            await self.bot.send_message(message.chat.id, "Database backup completed successfully.")
            
        #Handler for /startQuiz command
        @self.bot.message_handler(commands=['AdminHandler'])
        async def adminMsg(message):
            if str(message.from_user.id) != config.ADMIN_ID:
                await self.bot.send_message(message.chat.id, "Unauthorized. You are not an admin.")
                return
                
            if "ADD_QUESTION" in message.text:
                # Format: ADD_QUESTION: subject|level|question|option_a|option_b|option_c|option_d|correct_option
                lines = message.text.split("\n")
                count = 0
                errors = []
                for line in lines:
                    if "|" not in line: continue
                    try:
                        clean_line = line.replace("ADD_QUESTION:", "").strip()
                        data = clean_line.split("|")
                        if len(data) >= 8:
                            db_setup.add_question(*data[:8])
                            count += 1
                        else:
                            errors.append(f"Insufficient data in line: {line}")
                    except Exception as e:
                        errors.append(f"Error on {line}: {e}")
                
                response = f"Questions Added: {count}"
                if errors:
                    response += "\n\nErrors:\n" + "\n".join(errors)
                await self.bot.send_message(message.chat.id, response)

        # Handler for /startQuiz command
        @self.bot.message_handler(commands=['startQuiz'])
        async def start_quiz_handler(message):
            subjects = db_setup.get_subjects()
            markup = InlineKeyboardMarkup()
            for sub in subjects:
                markup.add(InlineKeyboardButton(sub, callback_data=f"quiz_start_{sub}"))
            markup.add(InlineKeyboardButton("Random Mix", callback_data="quiz_start_random"))
            
            await self.bot.send_message(message.chat.id, "Select a Quiz Subject:", reply_markup=markup)

        @self.bot.callback_query_handler(func=lambda call: call.data.startswith('quiz_start_'))
        async def callback_quiz_start(call):
            subject = call.data.replace('quiz_start_', '')
            if subject == "random": subject = None
            
            await self.bot.answer_callback_query(call.id, f"Starting {subject if subject else 'Random'} Quiz!")
            await self.bot.send_message(call.message.chat.id, f"Quiz Will start soon\n1. Total 10 Questions\n2. 15 Seconds per Question\n3. Correct +4, Wrong -1\n4. /QuitQuiz to exit.")
            
            await asyncio.sleep(2)
            userId = call.message.chat.id if call.message.chat.type in ['group', 'supergroup'] else call.from_user.id
            self.app.getUser(userId).trigger_quiz(subject=subject)
            
        # Handler for /QuitQuiz command
        @self.bot.message_handler(commands=['QuitQuiz'])
        async def quit_quiz(message):
            await self.bot.send_message(message.chat.id, "Quiz Ended.")
            userId = message.chat.id if message.chat.type in ['group', 'supergroup'] else message.from_user.id
            self.app.getUser(userId).finish_quiz()
        
        @self.bot.message_handler(func=lambda message: True)
        async def echo_message(message):
            self.check_and_register_user(message)

        # Update listener to handle poll answers
        @self.bot.poll_answer_handler()
        async def handle_poll_answer(poll_answer):
            user_id = poll_answer.user.id
            poll_id = poll_answer.poll_id
            selected_option = poll_answer.option_ids[0]
            QuizID = self.app.getQuizIdByPollId(poll_id)
            if QuizID != None:
                await self.app.getQuiz(QuizID).handle_poll_answer(poll_answer)
                LOG.INF(f"User {user_id} selected option {selected_option} in poll {poll_id}")
                self.app.getUser(user_id).heartbeat()
        
    async def set_commands(self):
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("startquiz", "Start a new quiz"),
            BotCommand("quitquiz", "Quit the current quiz"),
        ]
        await self.bot.set_my_commands(commands)
        LOG.INF("Bot commands set successfully")

    def run(self):
        asyncio.run(self.bot.polling())
        LOG.ERR("TELEGRAM_LISTENER_THREAD_EXITED !!!!FATAL")
    
    def check_and_register_user(self,message):
        chat_id = message.chat.id
        chat_type = message.chat.type
        self.app.getUser(message.from_user.id).heartbeat()
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

