# CaptchaGuard_tg_bot
Welcome!

This bot is designed to verify new users using CAPTCHA. Upon first interaction, it will send you a task to confirm you're not a bot.

🔹 Features:
✔ Automatic CAPTCHA for new users
✔ Easy integration with Telegram chats
✔ Built with aiogram (async Python framework)

This is my pet project, and I'd be happy if you find it useful! 🚀

Feel free to open an issue or fork the repo if you have suggestions or questions.

Here's a clean and professional **`README.md`** file in English for your project:

---

# 🤖 Telegram Bot Setup Guide

## 📋 Prerequisites
- Python 3.10+
- Git (optional)
- Telegram account

## 🚀 Quick Start

### 1. Clone the repository (if needed)
```bash
git clone https://github.com/yourusername/your-bot-repo.git
cd your-bot-repo
```

### 2. Set up environment
#### Create and activate virtual environment:
```bash
python -m venv .venv
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate
```

#### Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure the bot
Create `.env` file:
```bash
cp .env.example .env
```
Edit `.env` with your credentials:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_ID=your_telegram_id
DB_URL=sqlite+aiosqlite:///db.sqlite3
```

### 4. Get your credentials
- **BOT_TOKEN**: Get from [@BotFather](https://t.me/BotFather)
  - Type `/newbot` and follow instructions
- **ADMIN_ID**: Find your Telegram ID with [@userinfobot](https://t.me/userinfobot)

### 5. Run the bot
```bash
python main.py
```

## 🔧 Troubleshooting

### Common issues
1. **Missing dependencies**:
   ```bash
   pip install --upgrade -r requirements.txt
   ```

2. **Permission errors**:
   - On Linux/Mac:
     ```bash
     chmod +x start.sh
     ```

3. **Database problems**:
   - Delete `db.sqlite3` and restart the bot

## 🌟 Features
- Captcha system
- Anti-spam protection
- SQLite database

## 📜 License
MIT

---

### Additional files you might want:

#### `.env.example`
```env
# Bot token from @BotFather
BOT_TOKEN=your_token_here

# Your Telegram ID (get from @userinfobot)
ADMIN_ID=123456789

# Database connection
DB_URL=sqlite+aiosqlite:///db.sqlite3
```
This includes:
- Clear setup instructions
- Environment configuration
- Credentials guidance
- Basic troubleshooting
- File templates

Would you like me to add any specific sections (like deployment options or testing instructions)?
