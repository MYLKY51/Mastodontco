import os
from app import create_app, db
from app.models import User, ConstructionObject, Document, Settings
from datetime import datetime, timedelta
import random

def create_users():
    """Создает тестовых пользователей"""
    # Админ
    admin = User(
        username='admin',
        email='admin@example.com',
        is_admin=True,
        status='approved'
    )
    admin.set_password('adminpass')
    
    # Менеджеры проектов
    managers = [
        ('manager1', 'manager1@example.com'),
        ('manager2', 'manager2@example.com'),
        ('manager3', 'manager3@example.com')
    ]
    
    manager_objs = []
    for username, email in managers:
        manager = User(
            username=username,
            email=email,
            is_admin=True,
            status='approved'
        )
        manager.set_password('password')
        manager_objs.append(manager)
    
    # Обычные пользователи
    users = [
        ('user1', 'user1@example.com'),
        ('user2', 'user2@example.com'),
        ('user3', 'user3@example.com')
    ]
    
    user_objs = []
    for username, email in users:
        user = User(
            username=username,
            email=email,
            is_admin=False,
            status='approved'
        )
        user.set_password('password')
        user_objs.append(user)
    
    # Добавляем всех пользователей в сессию
    db.session.add(admin)
    for m in manager_objs:
        db.session.add(m)
    for u in user_objs:
        db.session.add(u)
    
    db.session.commit()
    
    return {
        'admin': admin,
        'managers': manager_objs,
        'users': user_objs
    }

def create_objects(managers):
    """Создает тестовые объекты строительства"""
    objects_data = [
        {
            'name': 'ЖК "Солнечный"',
            'address': 'г. Мурманск, ул. Солнечная, 12',
            'description': 'Многоэтажный жилой комплекс с подземной парковкой и благоустроенной территорией.',
            'status': 'active',
            'progress': 45,
            'start_date': datetime.now() - timedelta(days=90),
            'end_date': datetime.now() + timedelta(days=270)
        },
        {
            'name': 'ЖК "Морской"',
            'address': 'г. Мурманск, ул. Приморская, 24',
            'description': 'Комплекс апартаментов бизнес-класса с видом на залив и развитой инфраструктурой.',
            'status': 'construction',
            'progress': 70,
            'start_date': datetime.now() - timedelta(days=180),
            'end_date': datetime.now() + timedelta(days=90)
        },
        {
            'name': 'ЖК "Парковый"', 
            'address': 'г. Апатиты, пр. Ленина, 56',
            'description': 'Жилой комплекс эконом-класса рядом с городским парком.',
            'status': 'planning',
            'progress': 15,
            'start_date': datetime.now() + timedelta(days=30),
            'end_date': datetime.now() + timedelta(days=365)
        },
        {
            'name': 'ЖК "Ясный"',
            'address': 'г. Кандалакша, ул. Ясная, 8',
            'description': 'Малоэтажный жилой комплекс с индивидуальным отоплением.',
            'status': 'completed',
            'progress': 100,
            'start_date': datetime.now() - timedelta(days=365),
            'end_date': datetime.now() - timedelta(days=30)
        },
        {
            'name': 'ЖК "Центральный"',
            'address': 'г. Мончегорск, ул. Центральная, 15',
            'description': 'Многофункциональный комплекс в центре города с коммерческими помещениями.',
            'status': 'paused',
            'progress': 60,
            'start_date': datetime.now() - timedelta(days=150),
            'end_date': datetime.now() + timedelta(days=180)
        }
    ]
    
    objects = []
    for i, data in enumerate(objects_data):
        # Выбираем менеджера циклически
        manager = managers[i % len(managers)]
        
        obj = ConstructionObject(
            name=data['name'],
            address=data['address'],
            description=data['description'],
            status=data['status'],
            progress=data['progress'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            manager_id=manager.id
        )
        objects.append(obj)
        db.session.add(obj)
    
    db.session.commit()
    return objects

def create_documents(objects, users):
    """Создает тестовые документы для объектов"""
    # Типы документов
    doc_types = ['contract', 'permit', 'plan', 'report', 'other']
    
    # Автор документов - первый пользователь
    author = users[0]
    
    # Создаем несколько документов для каждого объекта
    for obj in objects:
        # 2-5 документов на объект
        num_docs = random.randint(2, 5)
        
        for i in range(num_docs):
            doc_type = random.choice(doc_types)
            doc_name = ""
            
            if doc_type == 'contract':
                doc_name = f"Договор подряда №{random.randint(100, 999)} - {obj.name}"
            elif doc_type == 'permit':
                doc_name = f"Разрешение на строительство №{random.randint(100, 999)} - {obj.name}"
            elif doc_type == 'plan':
                doc_name = f"План {random.choice(['первого', 'второго', 'третьего'])} этажа - {obj.name}"
            elif doc_type == 'report':
                doc_name = f"Отчет за {random.choice(['январь', 'февраль', 'март', 'апрель'])} 2023 - {obj.name}"
            else:
                doc_name = f"Спецификация материалов - {obj.name}"
                
            # Создаем запись о документе (без реального файла)
            doc = Document(
                name=doc_name,
                file_path=f"dummy_{random.randint(1000, 9999)}.pdf",
                file_extension="pdf",
                file_size=random.randint(100000, 5000000),  # 100KB - 5MB
                doc_type=doc_type,
                description=f"Тестовый документ для объекта {obj.name}",
                object_id=obj.id,
                uploaded_by_id=author.id,
                uploaded_at=datetime.now() - timedelta(days=random.randint(1, 60))
            )
            
            db.session.add(doc)
    
    db.session.commit()

def create_settings():
    """Создает начальные настройки системы"""
    settings = Settings(
        company_name="ООО Кольский Мастодонт",
        theme="light"
    )
    db.session.add(settings)
    db.session.commit()

def init_db():
    """Инициализирует базу данных тестовыми данными"""
    app = create_app()
    
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        
        # Проверяем, есть ли уже данные
        if User.query.count() == 0:
            print("Создаем тестовые данные...")
            
            # Создаем пользователей
            users = create_users()
            
            # Создаем объекты
            objects = create_objects(users['managers'])
            
            # Создаем документы
            create_documents(objects, users['users'])
            
            # Создаем настройки
            create_settings()
            
            print("База данных успешно инициализирована!")
        else:
            print("База данных уже содержит данные. Пропускаем инициализацию.")

if __name__ == "__main__":
    init_db() 