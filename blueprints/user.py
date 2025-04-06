from flask import Blueprint, session, redirect, url_for, render_template
from database import db_session
from database.models import User, UserLog

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    return f'Профиль пользователя: {user.first_name} {user.last_name}, {user.email}'

@user_bp.route('/user_logs')
def user_logs():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user = User.query.get(session['user_id'])
    logs = UserLog.query.filter_by(user_id=user.id).order_by(UserLog.timestamp.desc()).all()
    
    # В реальном приложении тут будет рендер шаблона
    log_list = '<br>'.join([f'{log.action} - {log.timestamp} - {log.ip_address}' for log in logs])
    return f'История активности пользователя {user.email}:<br>{log_list}' 