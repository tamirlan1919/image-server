from flask import Flask
from flask_cors import CORS
from config import Config
from utils import setup_logging, ensure_directories
from database import Database
from routes import register_routes


def create_app():
    app = Flask(__name__)
    #Настраиваем приложение
    app.config['SECTET_KEY'] = Config.SECRET_KEY
    app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

    CORS(app)

    with app.app_context():
        ensure_directories()
        setup_logging()

        #Database.init_db()
        print('База данных инциолзирована')
        print('Дирректории созданы')
        print('Логирование настроено')
    register_routes(app)
    return app

if __name__ == '__main__':
    print('Запуск сервера картинок')
    app = create_app()
    app.run(debug=Config.DEBUG)
