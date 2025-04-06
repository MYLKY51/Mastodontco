from flask import Blueprint, request, session, redirect, url_for, render_template
from database import db_session
from database.models import User, UserLog

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        
        # Проверка, что пользователь с таким email еще не существует
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return 'Пользователь с таким email уже существует'
        
        # Создание нового пользователя
        new_user = User(first_name=first_name, last_name=last_name, email=email)
        new_user.set_password(password)
        
        # Если загружен аватар
        if 'avatar' in request.files:
            avatar_file = request.files['avatar']
            if avatar_file.filename != '':
                new_user.avatar = avatar_file.read()
        
        db_session.add(new_user)
        db_session.commit()
        
        return redirect(url_for('auth.login'))
    
    return 'Форма регистрации'

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            
            # Логирование входа пользователя
            log_entry = UserLog(
                user_id=user.id,
                action='login',
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string
            )
            db_session.add(log_entry)
            db_session.commit()
            
            return redirect(url_for('user.profile'))
        
        return 'Неверный email или пароль'
    
    return 'Форма входа'

@auth_bp.route('/logout')
def logout():
    if 'user_id' in session:
        # Логирование выхода пользователя
        log_entry = UserLog(
            user_id=session['user_id'],
            action='logout',
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db_session.add(log_entry)
        db_session.commit()
        
        # Удаление из сессии
        session.pop('user_id', None)
    
    return redirect(url_for('auth.login')) 