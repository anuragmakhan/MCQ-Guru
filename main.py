import threading
import sys
import time

from src.utils import AppLogger as LOG
from src.bot import TelegramSender
from src.bot import TelegramReceiver
from src.core import InterThreadQueueHandler
from src.db import db_setup

def initialize_database():
    """Initialize the database tables and load default questions from files."""
    LOG.INF("Initializing database...")
    db_setup.create_tables()
    db_setup.init_questions_from_dir()
    LOG.INF("Database initialization complete.")

def main():
    LOG.INF("Starting MCQGuru Application...")
    
    # 1. Initialize the Database
    initialize_database()

    try:
        # 2. Start the Inter-Thread Queue Handler
        LOG.INF("Starting InterThreadQueueHandler...")
        InterThreadQueueHandler.InterThreadQueueHandler()

        # 3. Start the Telegram Receiver in a separate thread
        LOG.INF("Starting Telegram Receiver Bot...")
        receiver_bot = TelegramReceiver.TelegramReceiver()
        receiver_thread = threading.Thread(target=receiver_bot.run, daemon=True)
        receiver_thread.start()

        # 4. Start the Telegram Sender (Triggering Quiz Timers)
        LOG.INF("Initializing Telegram Sender & Timers...")
        sender_bot = TelegramSender.TelegramSender()
        sender_bot.triggerQuiz()

        LOG.INF("APPLICATION FULLY STARTED. Press Ctrl+C to exit.")
        
        # 5. Keep the main thread alive, waiting for the receiver thread
        # We loop with a timeout to allow KeyboardInterrupts to be caught promptly on Windows
        while receiver_thread.is_alive():
            receiver_thread.join(timeout=1.0)

    except KeyboardInterrupt:
        LOG.INF("Received shutdown signal. Exiting application gracefully...")
        import os
        os._exit(0)
    except Exception as e:
        LOG.ERR(f"Fatal error in main application: {e}")
        import os
        os._exit(1)

if __name__ == "__main__":
    main()
