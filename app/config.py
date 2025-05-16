import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    ADMIN_ID = int(os.getenv('ADMIN_ID'))
    REMNAWAVE_API_URL = os.getenv('REMNAWAVE_API_URL')
    REMNAWAVE_API_TOKEN = os.getenv('REMNAWAVE_API_TOKEN')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    ENV = os.getenv('ENV', 'development')
