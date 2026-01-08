import os
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from datetime import datetime
import uuid
import json
from io import BytesIO


HOST = 'localhost'
PORT = 8000

IMAGE_DIR = 'images'
LOGS_DIR = 'logs'


MAX_FILE_SIZE = 5 * 1024 * 1024 #5мб

ALLOWED_EXTENCIONS = {'.jpg', '.jpeg', '.png', '.gif'}
ALLOWED_MIME_TYPES = {
    'images/jpeg',
    'image/png',
    'image/gif'
}

LOG_FILE = os.path.join(LOGS_DIR, 'app.log')

def setup_logging():
    """Настройка логироания"""

    log_format = '[%(asctime)s] %(levelname)s: %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'

    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )


def log_info(message):
    """Логирует информационное сообщение"""
    logging.info(message)


def log_error(message):
    """Логирует сообщение об ошибке"""
    logging.error(message)


def log_success(message):
    """Логирует успешное действие"""
    logging.info(f'Успех: {message}')



def ensure_directories():
    """Создает необходимые папки если их нет"""
    os.makedirs(IMAGE_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)



class ImageServerHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP запросов для сервера изображений"""

    def do_GET(self):
        """Обработка гет запросов"""
        if self.path == '/':
            self.log("Запрос приветсвенной страницы")
            self.send_welcome_page()
        else:
            self.send_error_reponse(404, 'Маршрут не найден')
        
    
    def send_welcome_page(self):
        """Отправляет приветственное сообщение"""
        message = {
            'message': "Добро пожаловать на сервер изображений",
            'endpoints': {
                "GET /": "Эта страница",
                "POST /upload": "Загрузка изображений" 
            },
            "info": {
                "max_file_size": "5 Mb",
                "allowed_formats": list(ALLOWED_EXTENCIONS)
            }
        }
        self.send_json_response(200, message)

    def log(self, message, level='info'):
        """Логирует действие с информацией о запросе"""
        client_ip = self.client_address[0]
        log_messaage = f'{client_ip} - {self.command} - {self.path} - {message}'

        if level == 'error':
            log_error(log_messaage)
        else:
            log_info(log_messaage)

    
    def send_json_response(self, status_code, data):
        """Отправляет JSON ответ клиенту"""
        self.send_response(status_code)
        self.send_header('Content-Type', 'apllication/json; charset=utf-8')
        self.end_headers()
        
        response = json.dumps(data, ensure_ascii=False, indent=2)
        self.wfile.write(response.encode('utf-8'))



    def send_error_reponse(self, status_code, message):
        """Отправялет сообщение об ошибке"""
        error_data = {
            'error': message,
            "status_code": status_code
        }
        self.send_json_response(status_code, error_data)


    

if __name__ == '__main__':
    ensure_directories()

    setup_logging()

    server_adresess = (HOST, PORT)
    httpd = HTTPServer(server_adresess, ImageServerHandler)
    httpd.serve_forever()


