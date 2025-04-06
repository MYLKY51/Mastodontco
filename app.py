from flask import Flask
from database import db_session, init_db
import os

# Импорт блюпринтов
from blueprints.main import main_bp
from blueprints.auth import auth_bp
from blueprints.user import user_bp

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Регистрация блюпринтов
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
