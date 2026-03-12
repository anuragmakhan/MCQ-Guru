# 🎓 MCQ Guru - Telegram Quiz Bot

A feature-rich Telegram Quiz Bot built with Python and `pyTelegramBotAPI`. Designed for educational purposes, competitive exam preparation, and fun trivia.

## 🚀 Features

- **Dynamic Quiz Subjects**: Users can select specific categories (History, Geography, etc.) or play a random mix.
- **Real-time Scoring**: Integrated scoring system (+4 for correct, -1 for wrong).
- **Automated Timer**: Each question comes with a countdown timer to boost engagement.
- **Admin Dashboard**: Securely upload questions and back up the database directly via Telegram.
- **Modular Architecture**: Clean separation of concerns (Bot UI, Quiz Logic, Database, Utilities).
- **Environment Driven**: Fully configurable via `.env` files.

## 🛠️ Project Structure

```text
├── main.py             # Entry point
├── config.py           # Configuration loader
├── src/
│   ├── bot/            # Telegram Bot handlers
│   ├── core/           # Quiz and User logic
│   ├── db/             # SQLite Database operations
│   └── utils/          # Logger and shared types
├── tests/              # Unit tests
└── requirements.txt    # Dependencies
```

## ⚙️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/anuragmakhan/MCQ.git
   cd MCQ
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   - Rename `.env.example` to `.env`.
   - Add your `TELEGRAM_BOT_TOKEN` and `ADMIN_ID`.

4. **Initialize Database**:
   ```bash
   python src/db/db_setup.py
   ```

5. **Run the Bot**:
   ```bash
   python main.py
   ```

## 📝 Admin Usage

To upload questions, use the following template in a message to the bot:
`ADD_QUESTION: subject|level|question|option_a|option_b|option_c|option_d|correct_option`

## 🧪 Testing

Run tests using Pytest:
```bash
PYTHONPATH=. pytest
```

## 📜 License

MIT License. See `LICENSE` for details.
