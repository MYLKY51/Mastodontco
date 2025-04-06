# Mastodontco

Веб-приложение на Flask с модульной структурой и использованием блюпринтов.

## Структура проекта

```
mastodontco/
│
├── app/
│   ├── __init__.py          # Инициализация приложения
│   ├── main/                # Блюпринт основных страниц
│   │   ├── __init__.py
│   │   └── views.py
│   │
│   ├── api/                 # Блюпринт API
│   │   ├── __init__.py
│   │   └── views.py
│   │
│   ├── auth/                # Блюпринт аутентификации
│   │   ├── __init__.py
│   │   └── views.py
│   │
│   ├── models/              # Модели данных
│   │   ├── __init__.py
│   │   └── user.py
│   │
│   ├── static/              # Статические файлы
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── main.js
│   │
│   └── templates/           # Шаблоны
│       ├── index.html
│       └── auth/
│           ├── login.html
│           └── register.html
│
├── run.py                   # Запуск приложения
└── requirements.txt         # Зависимости
```

## Установка

1. Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

## Запуск приложения

```bash
python run.py
```

После запуска приложение будет доступно по адресу: http://127.0.0.1:5000/ 