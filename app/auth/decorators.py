from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def approval_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Если пользователь не авторизован, то это будет обработано декоратором login_required
        if current_user.is_authenticated and not current_user.is_approved():
            flash('Ваша учетная запись ожидает подтверждения администратором', 'warning')
            return redirect(url_for('auth.pending_approval'))
        return f(*args, **kwargs)
    return decorated_function 