from config import Config
from models import Image
from utils import (
    is_allowed_extension, format_file_size, get_file_extension,
    save_file, delete_file, log_error, log_success, log_info
)
from database import Database
from flask import render_template, request, jsonify, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename


def register_routes(app):
    """Региструем все маршируты в приложении Flask"""

    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return jsonify({'error': 'Файл не выбран'}), 400
        
        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': "Файл не выбран"}), 400
        
        if not is_allowed_extension(file.filename):
            return jsonify({'error': "Неподдерживаемый формат файла"}), 400
        
        try:
            file_data = file.read()
            file_size = len(file_data)

            if file_size > Config.MAX_CONTENT_LENGTH:
                max_size = format_file_size(Config.MAX_CONTENT_LENGTH)
                return jsonify({'error': f"Файл слишком большой. Максимум {max_size}"}), 400
            
            success, result = save_file(file_data, file.filename)

            if not success:
                return jsonify({'error': f"Ошибка сохранения: {result}"}), 500
            
            new_filename = result

            file_type = get_file_extension(file.filename).replace('.','')
            image = Image(
                filename=new_filename,
                original_name=secure_filename(file.filename),
                size=file_size,
                file_type=file_type
            )
            sueccess, image_id = Database.save_image(image)

            if not sueccess:
                delete_file(new_filename)
                return jsonify({'error': "Ошибка сохранения в БД"}), 500
            
            log_success(f'Изображение сохранено {new_filename}')

            return jsonify({
                'success': True,
                'message': "Файл успешно загружен",
                'image': {
                    'id': image_id,
                    'filename': new_filename,
                    'original_name': file.filename,
                    'size': format_file_size(file_size),
                    'url': f"/images/{new_filename}",
                    'delete_url': f'/delete/{image_id}'
                }
            }), 201
        except Exception as e:
            log_error(f'Ошибка загрузки файла: {e}')
            return jsonify({'error': str(e)}), 500
        
    @app.route('/delete/<int:image_id>')
    def delete_image(image_id=3)


http://localhost/delete/3

