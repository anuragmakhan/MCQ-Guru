import asyncio
import db_setup
import AppLogger as LOG
import appMain
import user
import threading

class TelegramReceiver:
    def __init__(self):
        self.app = appMain.appMain.get_instance()
        self.bot = self.app.ReceiverBot

        # Handler for /start command
        @self.bot.message_handler(commands=['start'])
        async def send_welcome(message):
            await self.bot.send_message(message.chat.id, "Welcome to the bot! \n स्वागत है MCQguru में! 📚परीक्षा की तैयारी, ज्ञान बढ़ाने या खुद को चुनौती देने के लिए यह बॉट आपके लिए एक आदर्श साथी है।.\n To Start Quiz -> /startQuiz")
            # Optionally, check and register the user when they send the /start command
            self.check_and_register_user(message)
            
        # Handler for /startQuiz command
        @self.bot.message_handler(commands=['AdminHandler'])
        async def adminMsg(message):
            if "ADD_QUESTION" in message.text:
                #db_setup.add_question("HISTORY","0","Which freedom fighter was known as the 'Lion of Punjab'?","Lala Lajpat Rai","Bhagat Singh","Udham Singh","Bal Gangadhar Tilak","Lala Lajpat Rai")
                QuestionList = message.text.split("\n")
                rplyString = "Not Added Question\n"
                count = 0
                for x in QuestionList:
                    print(x)
                    try:
                        db_setup.add_question(x)
                        count += 1
                        print("Added SUUU")
                    except Exception as e:
                        rplyString = rplyString + x + "\n" + "Error: " + str(e) + "\n"
                        
                await self.app.ReceiverBot.send_message(message.chat.id, "Question Added Successfully = "+ str(count) + "\n\n" + rplyString)

        # Handler for /startQuiz command
        @self.bot.message_handler(commands=['startQuiz'])
        async def send_welcome(message):
            await self.bot.send_message(message.chat.id, "Quiz Will start soon\n1. There will be total 10 Question\n2. Each Question Will Have 15 Seconds\n3. Correct answer +4 wrong answer -1\n4. Whenever want to Quit Quiz Press /QuitQuiz\n5. At the End of Quiz you will get result.")
            await asyncio.sleep(3)
            
            chat_type = message.chat.type
            if chat_type == 'group' or chat_type == 'supergroup':
                userId = message.chat.id
            else:
                userId = message.from_user.id
            self.app.getUser(userId).trigger_quiz()
            
        # Handler for /QuitQuiz command
        @self.bot.message_handler(commands=['QuitQuiz'])
        async def send_welcome(message):
            await self.bot.send_message(message.chat.id, "Thanks Quiz Ended, Will UPLOAD RESULT HERE")
            chat_type = message.chat.type
            if chat_type == 'group' or chat_type == 'supergroup':
                userId = message.chat.id
            else:
                userId = message.from_user.id
            self.app.getUser(userId).finish_quiz()
            #user.CurrentUser(message.chat.id).start_quiz()
        
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
        
    def run(self):
        asyncio.run(self.bot.polling())
        print("TELEGRAM_LISTENER_THREAD_EXITED !!!!FATAL")
    
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

