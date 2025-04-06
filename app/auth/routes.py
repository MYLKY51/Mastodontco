from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app.auth import bp
from app.models import User
from app import db

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Перенаправление, если пользователь уже авторизован
    if current_user.is_authenticated:
        if not current_user.is_approved():
            return redirect(url_for('auth.pending_approval'))
        return redirect(url_for('user.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember_me = 'remember_me' in request.form
        
        # Поиск пользователя по email
        user = User.query.filter_by(email=email).first()
        
        # Проверка пароля
        if user and user.check_password(password):
            login_user(user, remember=remember_me)
            
            # Если пользователь еще не подтвержден, отправляем на страницу ожидания
            if not user.is_approved():
                return redirect(url_for('auth.pending_approval'))
                
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('user.index')
            return redirect(next_page)
        else:
            flash('Неверный email или пароль', 'error')
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Перенаправление, если пользователь уже авторизован
    if current_user.is_authenticated:
        return redirect(url_for('user.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # Проверка заполнения всех полей
        if not all([username, email, password, password_confirm]):
            flash('Пожалуйста, заполните все поля', 'error')
            return render_template('auth/register.html')
        
        # Проверка совпадения паролей
        if password != password_confirm:
            flash('Пароли не совпадают', 'error')
            return render_template('auth/register.html')
        
        # Проверка, что пользователь с таким email или username не существует
        if User.query.filter_by(email=email).first():
            flash('Пользователь с таким email уже существует', 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует', 'error')
            return render_template('auth/register.html')
        
        # Создание нового пользователя
        user = User(username=username, email=email)
        user.set_password(password)
        
        # Сохранение пользователя в базе данных
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешно завершена! Теперь вы можете войти.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')

@bp.route('/pending-approval')
@login_required
def pending_approval():
    # Если пользователь уже подтвержден, перенаправляем на главную страницу
    if current_user.is_approved():
        return redirect(url_for('user.index'))
    
    return render_template('auth/pending_approval.html', user=current_user) 