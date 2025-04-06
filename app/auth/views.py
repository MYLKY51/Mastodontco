from flask import render_template, redirect, url_for, request, flash
from . import auth

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Здесь в будущем можно добавить проверку учетных данных
        # В текущей версии просто перенаправляем на dashboard
        return redirect(url_for('main.dashboard'))
    return render_template('auth/login.html')

@auth.route('/register')
def register():
    return render_template('auth/register.html') 