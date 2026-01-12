import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key')
    DEBUG = os.getenv('DEBUG', 'True').lower()

    #Настройка файлов
    UPLOAD_FOLDER = 'images'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024 #5мб
    ALLOWED_EXTENCIONS = {'.jpg', '.jpeg', '.png', '.gif'}
    ALLOWED_MIME_TYPES = {
        'image/jpeg',
        'image/png',
        'image/gif'
    }

    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/images_db')

    #Пагинация
    ITEMS_PER_PAGE = 10

    #Папки для хранения данных
    LOGS_DIR = 'logs'
    BACKUPS_DIR = 'backup'