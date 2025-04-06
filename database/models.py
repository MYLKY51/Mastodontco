import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary, Boolean
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from database import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    avatar = Column(LargeBinary, nullable=True)  # Хранение аватара в базе
    is_active = Column(Boolean, default=False)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Отношение к логам пользователя
    logs = relationship("UserLog", back_populates="user", cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'


class UserLog(Base):
    __tablename__ = 'user_logs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(String(50), nullable=False)  # login, logout, etc.
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(256), nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Отношение к пользователю
    user = relationship("User", back_populates="logs")
    
    def __repr__(self):
        return f'<UserLog {self.user_id} {self.action} at {self.timestamp}>' 