import os
from dotenv import load_dotenv

load_dotenv()

MAX_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BASE_URL = "https://platform-api.max.ru"