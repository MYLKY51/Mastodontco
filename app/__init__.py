# Empty file for package initialization

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Конфигурация приложения
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Инициализация расширений с приложением
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    with app.app_context():
        # Регистрация blueprint'ов
        from app.auth import bp as auth_bp
        app.register_blueprint(auth_bp)
        
        from app.admin import bp as admin_bp
        app.register_blueprint(admin_bp)
        
        from app.main import bp as main_bp
        app.register_blueprint(main_bp)
        
        # Создание базы данных, если она не существует
        db.create_all()
        
        # Импорт и регистрация моделей
        from app.models import User
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))
            
    return app