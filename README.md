# Default Aiogram Bot Template

A modern, feature-rich Telegram bot template built with [aiogram 3.x](https://aiogram.dev/) - a fully asynchronous framework for Telegram Bot API written in Python.

## ✨ Features

- 🚀 **Modern Architecture**: Built with aiogram 3.x for high performance and scalability
- 🛡️ **Admin Panel**: Web-based administrative interface for bot management
- 🗄️ **SQLite Database**: Lightweight, embedded database for data persistence
- ⚙️ **JSON Configuration**: Easy-to-modify configuration system via `config.json`
- 🔐 **Environment Variables**: Secure token management using `.env` file
- 📱 **Responsive Design**: Works seamlessly across different devices
- 🔄 **Async/Await**: Fully asynchronous codebase for optimal performance

## 📋 Requirements

- Python 3.8+
- pip (Python package manager)
- Telegram Bot Token (obtained from [@BotFather](https://t.me/BotFather))

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/mistaketz/default-aiogram.git
cd default-aiogram
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the root directory:

```env
BOT_TOKEN=your_bot_token_here
```

### 4. Configure the Bot

Edit `config.json` to customize your bot's behavior:

```json
{
   {
     "command": "start",
     "description": "Start the bot"
   },
   {
     "command": "help",
     "description": "Show help message"
   }
}
```

### 5. Run the Bot

```bash
python main.py
```

## 📁 Project Structure

```
default-aiogram/
├── database/
│   ├── model.py          # Simple ORM for sqlite database 
│   └── db.sqlite3        # Database 
├── handlers/
│   ├── __init__.py       # Initializer for other modules
│   ├── admin.py          # Admin handler
│   ├── ban.py            # Module to disallow use bot as restricted user
│   ├── callbacks.py      # Handler for callback queries
│   ├── commands.py       # Handler for commands
│   └── handler.py        # Handler for other messages
├── support/
│   ├── messages.py       # Module for sending messages with bot
│   ├── messages.json     # All messages for bot
│   └── config.json       # Bot configuration file
├── tasks/
│   ├── config.py         # Configuration for bot
│   ├── kb.py             # Message keyboard functions
│   ├── loader.py         # Loading the bot
│   ├── repetition.py     # Module for repeating tasks
│   └── states.py         # User states file
├── .gitignore            # Git ignore file
├── .env                  # Environment variables (create this)
├── example.env           # Environment variables example
├── requirements.txt      # Python dependencies
├── main.py               # Main bot entry point
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables (.env)

| Variable | Description | Required |
|----------|-------------|----------|
| `BOT_TOKEN` | Your Telegram Bot Token from BotFather | ✅ |

### Bot Configuration (config.json)

The `config.json` file allows you to customize:

- **Bot Commands**: Define available commands and their descriptions

### Admin Panel Features:

- 👥 **User Management**: View and manage bot users
- 📝 **Message Broadcasting**: Send messages to all users in specific time
- ⚙️ **Ban users**: Possibility to restric users
- 🗄️ **Database Management**: Backup and restore functionality

## 🗄️ Database

The bot uses SQLite as the default database, which is:

- **Lightweight**: No separate database server required
- **Portable**: Database file can be easily backed up and moved
- **Reliable**: ACID-compliant and battle-tested

### Database Models:

- **Users**: Store user information and preferences
- **Repetitions**: All broadcastings

## 🔌 Adding New Features

### Creating New Handlers

1. Create a new file in `handlers/`
2. Define your handler functions
3. Register handlers in the main dispatcher

Example:

```python
from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@dp.message(Command("mycommand"))
async def my_command_handler(message: types.Message):
    await sender.message(message.from_user.id, "hello_command")
```

## 🚀 Deployment

### Local Development

```bash
python main.py
```

### Production Deployment

1. **Using systemd** (Linux):

```bash
# Create service file
sudo nano /etc/systemd/system/telegram-bot.service

# Enable and start service
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

2. **Using Docker**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

3. **Using PM2**:

```bash
npm install -g pm2
pm2 start main.py --name telegram-bot --interpreter python3
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 **Documentation**: [Aiogram Documentation](https://docs.aiogram.dev/)
- 💬 **Telegram Chat**: [Aiogram Community](https://t.me/aiogram)
- 🐛 **Issues**: [GitHub Issues](https://github.com/mistaketz/default-aiogram/issues)

## 🎯 Roadmap

- [ ] Multi-language support (i18n)
- [ ] Advanced analytics dashboard
- [ ] Plugin system for easy extensibility
- [ ] Docker Compose setup
- [ ] Automated testing suite

---

**Made with ❤️ using [aiogram](https://aiogram.dev/)**