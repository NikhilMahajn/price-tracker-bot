import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
DB_NAME = os.getenv("DB_NAME")
TELEGRAM_API = os.getenv("TELEGRAM_API")
FLIPCART_PRICE_CLASS = os.getenv("FLIPCART_PRICE_CLASS")
FLIPCART_NAME_CLASS = os.getenv("FLIPCART_NAME_CLASS")