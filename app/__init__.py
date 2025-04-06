# Empty file for package initialization

import os
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__)
    
    # Конфигурация приложения
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(app.instance_path, 'mastodontco.sqlite'))
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Добавляем директорию для загрузки файлов
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB максимальный размер файла
    
    # Убедимся, что директория существует
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError:
        pass
    
    # Инициализация расширений с приложением
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите чтобы получить доступ к этой странице.'
    login_manager.login_message_category = 'warning'
    
    # Регистрация blueprints
    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.user import bp as user_bp
    app.register_blueprint(user_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
    
    # Route to redirect root to user interface
    @app.route('/')
    def index():
        return redirect(url_for('user.index'))
    
    return app