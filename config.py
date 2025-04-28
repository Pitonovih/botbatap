import os

# Токен бота из BotFather
API_TOKEN = '7755300043:AAG4qQiGk8MIZXIw4ecqZzWIoGVFlonnniY'  # Замените на ваш токен

# Путь к базе данных (НЕ ТРОГАТЬ)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cloud_storage.db')

# Максимальный размер файла (20 МБ)
MAX_FILE_SIZE = 20 * 1024 * 1024

# Настройки безопасности
PASSWORD_MIN_LENGTH = 4
PASSWORD_MAX_LENGTH = 32

# Emoji для интерфейса (НЕ ТРОГАТЬ)
EMOJI_PROTECTED = "🔒"
EMOJI_UNPROTECTED = "🔓"
EMOJI_FILE = "📄"
EMOJI_PHOTO = "🖼"
