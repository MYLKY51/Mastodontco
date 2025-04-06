from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_approved(self):
        return self.status == 'approved'
    
    def __repr__(self):
        return f'<User {self.username}>'
        
class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), default="ООО Кольский Мастодонт")
    logo_path = db.Column(db.String(255))
    theme = db.Column(db.String(10), default="light")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    def get_settings(cls):
        settings = cls.query.first()
        if not settings:
            settings = cls()
            db.session.add(settings)
            db.session.commit()
        return settings 

class ConstructionObject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='planning')  # planning, on_work, paused, completed
    progress = db.Column(db.Integer, default=0)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Внешние ключи
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Отношения
    manager = db.relationship('User', backref='managed_objects')
    documents = db.relationship('Document', backref='object', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def status_display(self):
        status_map = {
            'planning': 'Подготовка',
            'active': 'Активный',
            'construction': 'Строительство',
            'paused': 'Приостановлен',
            'completed': 'Завершен'
        }
        return status_map.get(self.status, self.status)
    
    def __repr__(self):
        return f'<ConstructionObject {self.name}>'

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    file_extension = db.Column(db.String(10))
    file_size = db.Column(db.Integer)  # размер в байтах
    doc_type = db.Column(db.String(20))  # contract, permit, plan, report, other
    description = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Внешние ключи
    object_id = db.Column(db.Integer, db.ForeignKey('construction_object.id'))
    uploaded_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Отношения
    uploaded_by = db.relationship('User', backref='uploaded_documents')
    
    @property
    def doc_type_display(self):
        type_map = {
            'contract': 'Договор',
            'permit': 'Разрешение',
            'plan': 'План',
            'report': 'Отчет',
            'other': 'Прочее'
        }
        return type_map.get(self.doc_type, self.doc_type)
    
    @property
    def size(self):
        if not self.file_size:
            return "0 KB"
        
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024 or unit == 'GB':
                return f"{size:.2f} {unit}".replace('.00', '')
            size /= 1024
    
    def __repr__(self):
        return f'<Document {self.name}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 