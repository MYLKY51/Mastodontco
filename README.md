# Mastodontco - Система управления строительными объектами

Веб-приложение для управления строительными объектами и документацией.

## Функциональность

- **Администраторы**: управление объектами строительства, загрузка и просмотр документов, контроль доступа пользователей
- **Пользователи**: просмотр объектов строительства, доступ к документации, отслеживание прогресса

## Установка и запуск

### Требования
- Python 3.8+
- Flask и зависимости (см. requirements.txt)

### Настройка среды

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/mastodontco.git
cd mastodontco
```

2. Создайте и активируйте виртуальное окружение:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл .env с переменными окружения:
```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///instance/mastodontco.sqlite
```

### Инициализация базы данных

1. Создайте директорию для базы данных и загрузок:
```bash
mkdir -p instance/uploads
```

2. Выполните инициализацию базы данных с тестовыми данными:
```bash
python init_db.py
```

### Запуск приложения

```bash
# Для разработки
flask run --debug

# Для продакшена
gunicorn 'app:create_app()'
```

## Доступ к приложению

После запуска приложение доступно по адресу: http://localhost:5000

### Тестовые учетные записи:

| Роль | Логин | Пароль |
|------|-------|--------|
| Администратор | admin | adminpass |
| Менеджер | manager1 | password |
| Пользователь | user1 | password |

## Структура проекта

- `app/` - основной пакет приложения
  - `admin/` - административная часть
  - `user/` - пользовательская часть
  - `auth/` - аутентификация
  - `models.py` - модели данных
  - `templates/` - шаблоны
  - `static/` - статические файлы
- `instance/` - данные экземпляра (база данных, загрузки)
- `migrations/` - скрипты миграции базы данных
- `init_db.py` - скрипт инициализации базы данных

## Лицензия

©2023 ООО "Кольский Мастодонт". Все права защищены. 