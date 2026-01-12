import psycopg2

from typing import List, Tuple, Optional
from config import Config
from models import Image
from utils import log_info, log_error, log_success


class Database():

    @staticmethod
    def get_connection():
        return psycopg2.connect(Config.DATABASE_URL)
    
    @staticmethod
    def init_db():
        conn = Database.get_connection()
        try:
            pass