from flask import render_template, redirect, url_for, request, flash, current_app
from app.admin import bp
from datetime import datetime, timedelta
from app.models import User, ConstructionObject, Document
from app import db
from app.admin.forms import ConstructionObjectForm, DocumentForm
import os
from werkzeug.utils import secure_filename
import uuid

@bp.route('/')
def index():
    # Заглушки для данных (в реальном приложении эти данные нужно получать из базы данных)
    stats = {
        'users_count': 250,
        'users_growth': 12,
        'objects_count': 42,
        'objects_growth': 8,
        'reports_count': 125,
        'reports_growth': 15,
        'messages_count': 752,
        'messages_growth': -3
    }
    
    # Заглушка для новых пользователей
    new_users = [
        {
            'name': 'Иван Петров',
            'initials': 'ИП',
            'avatar': None,
            'role': 'Менеджер',
            'joined': 'Сегодня'
        },
        {
            'name': 'Анна Смирнова',
            'initials': 'АС',
            'avatar': None,
            'role': 'Клиент',
            'joined': 'Вчера'
        },
        {
            'name': 'Сергей Иванов',
            'initials': 'СИ',
            'avatar': None,
            'role': 'Подрядчик',
            'joined': '2 дня назад'
        }
    ]
    
    # Заглушка для последних действий
    recent_actions = [
        {
            'user': {
                'name': 'Иван Петров',
                'avatar': None
            },
            'description': 'Создал новый объект',
            'object': 'ЖК "Солнечный"',
            'time': '5 минут назад'
        },
        {
            'user': {
                'name': 'Анна Смирнова',
                'avatar': None
            },
            'description': 'Загрузила фотоотчет',
            'object': 'ЖК "Морской"',
            'time': '20 минут назад'
        },
        {
            'user': {
                'name': 'Сергей Иванов',
                'avatar': None
            },
            'description': 'Обновил статус задачи',
            'object': 'ЖК "Парковый"',
            'time': '1 час назад'
        },
        {
            'user': {
                'name': 'Мария Козлова',
                'avatar': None
            },
            'description': 'Добавила комментарий',
            'object': 'ЖК "Ясный"',
            'time': '3 часа назад'
        }
    ]
    
    # Конфигурация админ-эндпоинтов (для отображения ссылок в меню)
    admin_endpoints = {
        'admin.index': True,
        'admin.users': True,
        'admin.objects': True,
        'admin.docs': True,
        'admin.photos': True,
        'admin.chat': True
    }
    
    return render_template(
        'admin/index.html', 
        stats=stats, 
        new_users=new_users,
        recent_actions=recent_actions,
        config={'ADMIN_ENDPOINTS': admin_endpoints}
    )

@bp.route('/users')
def users():
    # Заглушка для списка пользователей
    users_list = [
        {
            'id': 1,
            'name': 'Иван Петров',
            'initials': 'ИП',
            'email': 'i.petrov@example.com',
            'phone': '+7 (900) 123-45-67',
            'role': 'admin',
            'role_display': 'Администратор',
            'status': 'active',
            'status_display': 'Активен',
            'registered_at': '12.02.2023',
            'avatar': None
        },
        {
            'id': 2,
            'name': 'Анна Смирнова',
            'initials': 'АС',
            'email': 'a.smirnova@example.com',
            'phone': '+7 (900) 234-56-78',
            'role': 'manager',
            'role_display': 'Менеджер',
            'status': 'active',
            'status_display': 'Активен',
            'registered_at': '15.03.2023',
            'avatar': None
        },
        {
            'id': 3,
            'name': 'Сергей Иванов',
            'initials': 'СИ',
            'email': 's.ivanov@example.com',
            'phone': '+7 (900) 345-67-89',
            'role': 'client',
            'role_display': 'Клиент',
            'status': 'inactive',
            'status_display': 'Неактивен',
            'registered_at': '01.04.2023',
            'avatar': None
        },
        {
            'id': 4,
            'name': 'Мария Козлова',
            'initials': 'МК',
            'email': 'm.kozlova@example.com',
            'phone': '+7 (900) 456-78-90',
            'role': 'contractor',
            'role_display': 'Подрядчик',
            'status': 'active',
            'status_display': 'Активен',
            'registered_at': '10.05.2023',
            'avatar': None
        },
        {
            'id': 5,
            'name': 'Дмитрий Соколов',
            'initials': 'ДС',
            'email': 'd.sokolov@example.com',
            'phone': None,
            'role': 'client',
            'role_display': 'Клиент',
            'status': 'banned',
            'status_display': 'Заблокирован',
            'registered_at': '22.06.2023',
            'avatar': None
        }
    ]
    
    # Данные для пагинации
    pagination = {
        'start': 1,
        'end': 5,
        'total': 25,
        'current': 1,
        'pages': [1, 2, 3, 4, 5]
    }
    
    # Данные для настройки меню
    admin_endpoints = {
        'admin.index': True,
        'admin.users': True,
        'admin.objects': True,
        'admin.docs': True,
        'admin.photos': True,
        'admin.chat': True
    }
    
    return render_template(
        'admin/users.html',
        users=users_list,
        pagination=pagination,
        config={'ADMIN_ENDPOINTS': admin_endpoints}
    )

@bp.route('/objects')
def objects():
    # Получаем все объекты
    objects = ConstructionObject.query.all()
    
    # Получаем менеджеров для фильтра
    managers = User.query.filter(User.is_admin == True).all()
    
    # Заглушка для пагинации
    pagination = {
        'total': len(objects),
        'start': 1,
        'end': len(objects),
        'current': 1,
        'pages': [1]
    }
    
    return render_template(
        'admin/objects.html',
        objects=objects,
        managers=managers,
        pagination=pagination
    )

@bp.route('/objects/create', methods=['GET', 'POST'])
def create_object():
    form = ConstructionObjectForm()
    
    if form.validate_on_submit():
        new_object = ConstructionObject(
            name=form.name.data,
            address=form.address.data,
            description=form.description.data,
            status=form.status.data,
            progress=form.progress.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            manager_id=form.manager_id.data
        )
        db.session.add(new_object)
        db.session.commit()
        
        flash(f'Объект "{new_object.name}" успешно создан', 'success')
        return redirect(url_for('admin.objects'))
    
    return render_template(
        'admin/object_form.html',
        form=form,
        title='Создание нового объекта'
    )

@bp.route('/objects/<int:object_id>/edit', methods=['GET', 'POST'])
def edit_object(object_id):
    obj = ConstructionObject.query.get_or_404(object_id)
    form = ConstructionObjectForm(obj=obj)
    
    if request.method == 'GET':
        # Заполняем форму данными из объекта
        form.name.data = obj.name
        form.address.data = obj.address
        form.description.data = obj.description
        form.status.data = obj.status
        form.progress.data = obj.progress
        form.start_date.data = obj.start_date
        form.end_date.data = obj.end_date
        form.manager_id.data = obj.manager_id
    
    if form.validate_on_submit():
        obj.name = form.name.data
        obj.address = form.address.data
        obj.description = form.description.data
        obj.status = form.status.data
        obj.progress = form.progress.data
        obj.start_date = form.start_date.data
        obj.end_date = form.end_date.data
        obj.manager_id = form.manager_id.data
        obj.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash(f'Объект "{obj.name}" успешно обновлен', 'success')
        return redirect(url_for('admin.objects'))
    
    return render_template(
        'admin/object_form.html',
        form=form,
        title=f'Редактирование объекта "{obj.name}"',
        object=obj
    )

@bp.route('/objects/<int:object_id>/delete', methods=['POST'])
def delete_object(object_id):
    obj = ConstructionObject.query.get_or_404(object_id)
    
    # Сохраняем имя для сообщения
    object_name = obj.name
    
    # Удаляем связанные документы (файлы)
    for doc in obj.documents:
        try:
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            current_app.logger.error(f'Ошибка при удалении файла {doc.file_path}: {str(e)}')
    
    # Удаляем объект из базы (документы удалятся каскадно)
    db.session.delete(obj)
    db.session.commit()
    
    flash(f'Объект "{object_name}" и все связанные документы успешно удалены', 'success')
    return redirect(url_for('admin.objects'))

@bp.route('/docs')
def docs():
    # Получаем все документы
    documents = Document.query.all()
    
    # Получаем объекты для фильтра
    objects = ConstructionObject.query.all()
    
    # Заглушка для пагинации
    pagination = {
        'total': len(documents),
        'start': 1,
        'end': len(documents),
        'current': 1,
        'pages': [1]
    }
    
    return render_template(
        'admin/docs.html',
        documents=documents,
        objects=objects,
        pagination=pagination
    )

@bp.route('/docs/create', methods=['GET', 'POST'])
def create_document():
    form = DocumentForm()
    # Динамически заполняем список объектов
    form.object_id.choices = [(o.id, o.name) for o in ConstructionObject.query.all()]
    
    if form.validate_on_submit():
        # Обработка загруженного файла
        file = form.file.data
        filename = secure_filename(file.filename)
        # Создаем уникальное имя файла для избежания коллизий
        unique_filename = str(uuid.uuid4()) + '_' + filename
        
        # Получаем расширение файла
        file_ext = os.path.splitext(filename)[1][1:].lower()
        
        # Создаем директорию для загрузок, если ее нет
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Полный путь для сохранения файла
        file_path = os.path.join(upload_folder, unique_filename)
        
        # Сохраняем файл
        file.save(file_path)
        
        # Создаем запись о документе
        new_document = Document(
            name=form.name.data,
            file_path=unique_filename,
            file_extension=file_ext,
            file_size=os.path.getsize(file_path),
            doc_type=form.doc_type.data,
            description=form.description.data,
            object_id=form.object_id.data,
            uploaded_by_id=1  # Заглушка, в реальном приложении используйте current_user.id
        )
        
        db.session.add(new_document)
        db.session.commit()
        
        flash(f'Документ "{new_document.name}" успешно загружен', 'success')
        return redirect(url_for('admin.docs'))
    
    return render_template(
        'admin/document_form.html',
        form=form,
        title='Загрузка нового документа'
    )

@bp.route('/docs/<int:doc_id>/edit', methods=['GET', 'POST'])
def edit_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    form = DocumentForm()
    form.object_id.choices = [(o.id, o.name) for o in ConstructionObject.query.all()]
    
    # При GET запросе заполняем форму данными из документа
    if request.method == 'GET':
        form.name.data = doc.name
        form.object_id.data = doc.object_id
        form.doc_type.data = doc.doc_type
        form.description.data = doc.description
        # Не заполняем поле файла, так как это потребует повторной загрузки
    
    if form.validate_on_submit():
        # Обновляем базовую информацию
        doc.name = form.name.data
        doc.object_id = form.object_id.data
        doc.doc_type = form.doc_type.data
        doc.description = form.description.data
        
        # Если загружен новый файл, обрабатываем его
        if form.file.data:
            # Удаляем старый файл
            try:
                old_file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.file_path)
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)
            except Exception as e:
                current_app.logger.error(f'Ошибка при удалении файла {doc.file_path}: {str(e)}')
            
            # Обрабатываем новый файл
            file = form.file.data
            filename = secure_filename(file.filename)
            unique_filename = str(uuid.uuid4()) + '_' + filename
            file_ext = os.path.splitext(filename)[1][1:].lower()
            
            # Сохраняем новый файл
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(file_path)
            
            # Обновляем информацию о файле
            doc.file_path = unique_filename
            doc.file_extension = file_ext
            doc.file_size = os.path.getsize(file_path)
        
        db.session.commit()
        
        flash(f'Документ "{doc.name}" успешно обновлен', 'success')
        return redirect(url_for('admin.docs'))
    
    return render_template(
        'admin/document_form.html',
        form=form,
        title=f'Редактирование документа "{doc.name}"',
        document=doc
    )

@bp.route('/docs/<int:doc_id>/delete', methods=['POST'])
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    
    # Сохраняем имя для сообщения
    doc_name = doc.name
    
    # Удаляем файл
    try:
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], doc.file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        current_app.logger.error(f'Ошибка при удалении файла {doc.file_path}: {str(e)}')
    
    # Удаляем запись о документе
    db.session.delete(doc)
    db.session.commit()
    
    flash(f'Документ "{doc_name}" успешно удален', 'success')
    return redirect(url_for('admin.docs'))

@bp.route('/objects/<int:object_id>/docs')
def object_docs(object_id):
    obj = ConstructionObject.query.get_or_404(object_id)
    documents = Document.query.filter_by(object_id=object_id).all()
    
    return render_template(
        'admin/object_docs.html',
        object=obj,
        documents=documents
    )

@bp.route('/objects/<int:object_id>/add_doc', methods=['GET', 'POST'])
def add_document_to_object(object_id):
    obj = ConstructionObject.query.get_or_404(object_id)
    form = DocumentForm()
    # Устанавливаем объект по умолчанию и скрываем поле
    form.object_id.choices = [(obj.id, obj.name)]
    form.object_id.data = obj.id
    
    if form.validate_on_submit():
        # Обработка загруженного файла
        file = form.file.data
        filename = secure_filename(file.filename)
        unique_filename = str(uuid.uuid4()) + '_' + filename
        file_ext = os.path.splitext(filename)[1][1:].lower()
        
        # Создаем директорию для загрузок, если ее нет
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        # Полный путь для сохранения файла
        file_path = os.path.join(upload_folder, unique_filename)
        
        # Сохраняем файл
        file.save(file_path)
        
        # Создаем запись о документе
        new_document = Document(
            name=form.name.data,
            file_path=unique_filename,
            file_extension=file_ext,
            file_size=os.path.getsize(file_path),
            doc_type=form.doc_type.data,
            description=form.description.data,
            object_id=obj.id,
            uploaded_by_id=1  # Заглушка, в реальном приложении используйте current_user.id
        )
        
        db.session.add(new_document)
        db.session.commit()
        
        flash(f'Документ "{new_document.name}" успешно добавлен к объекту "{obj.name}"', 'success')
        return redirect(url_for('admin.object_docs', object_id=obj.id))
    
    return render_template(
        'admin/document_form.html',
        form=form,
        title=f'Добавление документа к объекту "{obj.name}"',
        object=obj,
        hide_object_field=True
    )

@bp.route('/photos')
def photos():
    # Заглушка для списка фотоотчетов
    photo_reports = [
        {
            'id': 1,
            'object_id': 1,
            'object_name': 'ЖК "Солнечный"',
            'title': 'Заливка фундамента, блок А',
            'description': 'Завершение работ по заливке фундамента жилого блока А.',
            'date': '15.03.2023',
            'status': 'pending',
            'status_display': 'На проверке',
            'author': {
                'name': 'Сергей Иванов',
                'initials': 'СИ',
                'avatar': None
            },
            'photos_count': 5,
            'preview_image': None
        },
        {
            'id': 2,
            'object_id': 2,
            'object_name': 'ЖК "Морской"',
            'title': 'Монтаж перекрытий 3-го этажа',
            'description': 'Монтаж плит перекрытия на 3-м этаже завершен на 85%.',
            'date': '20.03.2023',
            'status': 'approved',
            'status_display': 'Подтвержден',
            'author': {
                'name': 'Анна Смирнова',
                'initials': 'АС',
                'avatar': None
            },
            'photos_count': 8,
            'preview_image': None
        },
        {
            'id': 3,
            'object_id': 1,
            'object_name': 'ЖК "Солнечный"',
            'title': 'Прокладка коммуникаций',
            'description': 'Завершены работы по прокладке основных коммуникаций в блоке Б.',
            'date': '25.03.2023',
            'status': 'rejected',
            'status_display': 'Отклонен',
            'author': {
                'name': 'Иван Петров',
                'initials': 'ИП',
                'avatar': None
            },
            'photos_count': 3,
            'preview_image': None,
            'rejection_reason': 'Недостаточно фотографий для подтверждения объема работ'
        },
        {
            'id': 4,
            'object_id': 3,
            'object_name': 'ЖК "Парковый"',
            'title': 'Подготовка площадки',
            'description': 'Подготовительные работы на строительной площадке.',
            'date': '01.04.2023',
            'status': 'pending',
            'status_display': 'На проверке',
            'author': {
                'name': 'Мария Козлова',
                'initials': 'МК',
                'avatar': None
            },
            'photos_count': 10,
            'preview_image': None
        },
        {
            'id': 5,
            'object_id': 2,
            'object_name': 'ЖК "Морской"',
            'title': 'Фасадные работы',
            'description': 'Начало работ по монтажу вентилируемого фасада.',
            'date': '05.04.2023',
            'status': 'approved',
            'status_display': 'Подтвержден',
            'author': {
                'name': 'Анна Смирнова',
                'initials': 'АС',
                'avatar': None
            },
            'photos_count': 6,
            'preview_image': None
        }
    ]
    
    # Список объектов для фильтра
    objects = [
        {'id': 1, 'name': 'ЖК "Солнечный"'},
        {'id': 2, 'name': 'ЖК "Морской"'},
        {'id': 3, 'name': 'ЖК "Парковый"'},
        {'id': 4, 'name': 'ЖК "Ясный"'},
        {'id': 5, 'name': 'ЖК "Центральный"'}
    ]
    
    # Данные для пагинации
    pagination = {
        'start': 1,
        'end': 5,
        'total': 12,
        'current': 1,
        'pages': [1, 2, 3]
    }
    
    # Данные для настройки меню
    admin_endpoints = {
        'admin.index': True,
        'admin.users': True,
        'admin.objects': True,
        'admin.docs': True,
        'admin.photos': True,
        'admin.chat': True
    }
    
    return render_template(
        'admin/photos.html',
        photo_reports=photo_reports,
        objects=objects,
        pagination=pagination,
        config={'ADMIN_ENDPOINTS': admin_endpoints}
    )

@bp.route('/chat')
def chat():
    # Заглушка для сообщений чата
    chat_messages = [
        {
            'id': 1,
            'text': 'Когда будет завершена отделка фасада блока А?',
            'sender': {
                'name': 'Анна Смирнова',
                'initials': 'АС',
                'avatar': None,
                'role': 'manager',
                'role_display': 'Менеджер'
            },
            'timestamp': '01.04.2023 10:15',
            'status': 'active',
            'status_display': 'Активно',
            'object': {
                'id': 2,
                'name': 'ЖК "Морской"'
            },
            'chat_type': 'object',
            'chat_type_display': 'Объект',
            'attachment': None
        },
        {
            'id': 2,
            'text': 'Что за проблема с вентиляцией? Техзадание составлено было четко и согласовано со всеми!',
            'sender': {
                'name': 'Иван Петров',
                'initials': 'ИП',
                'avatar': None,
                'role': 'contractor',
                'role_display': 'Подрядчик'
            },
            'timestamp': '01.04.2023 11:30',
            'status': 'flagged',
            'status_display': 'Помечено',
            'object': {
                'id': 1,
                'name': 'ЖК "Солнечный"'
            },
            'chat_type': 'object',
            'chat_type_display': 'Объект',
            'attachment': None,
            'flag_reason': 'Возможный конфликт'
        },
        {
            'id': 3,
            'text': 'Подскажите, когда можно прийти на осмотр квартиры? Ключи уже можно получить?',
            'sender': {
                'name': 'Сергей Иванов',
                'initials': 'СИ',
                'avatar': None,
                'role': 'client',
                'role_display': 'Клиент'
            },
            'timestamp': '01.04.2023 12:45',
            'status': 'active',
            'status_display': 'Активно',
            'object': {
                'id': 4,
                'name': 'ЖК "Ясный"'
            },
            'chat_type': 'support',
            'chat_type_display': 'Поддержка',
            'attachment': None
        },
        {
            'id': 4,
            'text': 'Какого черта строительство опять приостановлено? Это уже третий раз за месяц!',
            'sender': {
                'name': 'Дмитрий Соколов',
                'initials': 'ДС',
                'avatar': None,
                'role': 'client',
                'role_display': 'Клиент'
            },
            'timestamp': '01.04.2023 14:20',
            'status': 'blocked',
            'status_display': 'Заблокировано',
            'object': {
                'id': 5,
                'name': 'ЖК "Центральный"'
            },
            'chat_type': 'support',
            'chat_type_display': 'Поддержка',
            'attachment': None,
            'block_reason': 'Нецензурная лексика',
            'blocked_by': {
                'name': 'Мария Козлова',
                'initials': 'МК',
                'avatar': None
            },
            'blocked_at': '01.04.2023 14:25'
        },
        {
            'id': 5,
            'text': 'Могу прислать фотографии проблемы с трубами в санузле. Нужно срочно исправить до заливки стяжки.',
            'sender': {
                'name': 'Алексей Николаев',
                'initials': 'АН',
                'avatar': None,
                'role': 'contractor',
                'role_display': 'Подрядчик'
            },
            'timestamp': '01.04.2023 15:10',
            'status': 'active',
            'status_display': 'Активно',
            'object': {
                'id': 3,
                'name': 'ЖК "Парковый"'
            },
            'chat_type': 'object',
            'chat_type_display': 'Объект',
            'attachment': {
                'type': 'image',
                'url': None,
                'name': 'pipes_issue.jpg',
                'size': '2.4 МБ'
            }
        }
    ]
    
    # Список объектов для фильтра
    objects = [
        {'id': 1, 'name': 'ЖК "Солнечный"'},
        {'id': 2, 'name': 'ЖК "Морской"'},
        {'id': 3, 'name': 'ЖК "Парковый"'},
        {'id': 4, 'name': 'ЖК "Ясный"'},
        {'id': 5, 'name': 'ЖК "Центральный"'}
    ]
    
    # Данные для пагинации
    pagination = {
        'start': 1,
        'end': 5,
        'total': 28,
        'current': 1,
        'pages': [1, 2, 3, 4]
    }
    
    # Данные для настройки меню
    admin_endpoints = {
        'admin.index': True,
        'admin.users': True,
        'admin.objects': True,
        'admin.docs': True,
        'admin.photos': True,
        'admin.chat': True
    }
    
    return render_template(
        'admin/chat.html',
        chat_messages=chat_messages,
        objects=objects,
        pagination=pagination,
        config={'ADMIN_ENDPOINTS': admin_endpoints}
    )

@bp.route('/photos/<int:report_id>')
def photo_report_detail(report_id):
    # Заглушка для детальной информации о фотоотчете
    report = None
    
    # Заглушка для списка фотоотчетов
    all_reports = [
        {
            'id': 1,
            'object_id': 1,
            'object_name': 'ЖК "Солнечный"',
            'title': 'Заливка фундамента, блок А',
            'description': 'Завершение работ по заливке фундамента жилого блока А.',
            'date': '15.03.2023',
            'status': 'pending',
            'status_display': 'На проверке',
            'author': {
                'name': 'Сергей Иванов',
                'initials': 'СИ',
                'avatar': None
            },
            'photos_count': 5,
            'preview_image': None,
            'photos': [
                {'id': 1, 'url': None, 'description': 'Подготовка опалубки'},
                {'id': 2, 'url': None, 'description': 'Армирование фундамента'},
                {'id': 3, 'url': None, 'description': 'Заливка бетона'},
                {'id': 4, 'url': None, 'description': 'Выравнивание поверхности'},
                {'id': 5, 'url': None, 'description': 'Готовый фундамент'}
            ]
        },
        {
            'id': 2,
            'object_id': 2,
            'object_name': 'ЖК "Морской"',
            'title': 'Монтаж перекрытий 3-го этажа',
            'description': 'Монтаж плит перекрытия на 3-м этаже завершен на 85%.',
            'date': '20.03.2023',
            'status': 'approved',
            'status_display': 'Подтвержден',
            'author': {
                'name': 'Анна Смирнова',
                'initials': 'АС',
                'avatar': None
            },
            'photos_count': 8,
            'preview_image': None,
            'photos': [
                {'id': 6, 'url': None, 'description': 'Подъем плиты краном'},
                {'id': 7, 'url': None, 'description': 'Установка плиты'},
                {'id': 8, 'url': None, 'description': 'Выравнивание по уровню'},
                {'id': 9, 'url': None, 'description': 'Крепление к несущим элементам'},
                {'id': 10, 'url': None, 'description': 'Заполнение швов раствором'},
                {'id': 11, 'url': None, 'description': 'Проверка качества укладки'},
                {'id': 12, 'url': None, 'description': 'Вид с высоты на уложенные плиты'},
                {'id': 13, 'url': None, 'description': 'Общий вид этажа после монтажа'}
            ],
            'approved_by': {
                'name': 'Дмитрий Соколов',
                'initials': 'ДС',
                'avatar': None
            },
            'approved_at': '21.03.2023',
            'approval_comment': 'Работы выполнены в соответствии с проектной документацией'
        },
        {
            'id': 3,
            'object_id': 1,
            'object_name': 'ЖК "Солнечный"',
            'title': 'Прокладка коммуникаций',
            'description': 'Завершены работы по прокладке основных коммуникаций в блоке Б.',
            'date': '25.03.2023',
            'status': 'rejected',
            'status_display': 'Отклонен',
            'author': {
                'name': 'Иван Петров',
                'initials': 'ИП',
                'avatar': None
            },
            'photos_count': 3,
            'preview_image': None,
            'photos': [
                {'id': 14, 'url': None, 'description': 'Траншея для прокладки труб'},
                {'id': 15, 'url': None, 'description': 'Укладка канализационных труб'},
                {'id': 16, 'url': None, 'description': 'Подключение к магистральному коллектору'}
            ],
            'rejected_by': {
                'name': 'Дмитрий Соколов',
                'initials': 'ДС',
                'avatar': None
            },
            'rejected_at': '26.03.2023',
            'rejection_reason': 'Недостаточно фотографий для подтверждения объема работ. Нет фотографий водопровода и электрических кабелей.'
        }
    ]
    
    # Находим отчет по ID
    for r in all_reports:
        if r['id'] == report_id:
            report = r
            break
    
    if not report:
        # Если отчет не найден, перенаправляем на список отчетов
        return redirect(url_for('admin.photos'))
    
    # Данные для настройки меню
    admin_endpoints = {
        'admin.index': True,
        'admin.users': True,
        'admin.objects': True,
        'admin.docs': True,
        'admin.photos': True,
        'admin.chat': True
    }
    
    return render_template(
        'admin/photo_report_detail.html',
        report=report,
        config={'ADMIN_ENDPOINTS': admin_endpoints}
    )

@bp.route('/photos/<int:report_id>/approve', methods=['POST'])
def approve_photo_report(report_id):
    # В реальном приложении здесь будет обновление статуса в базе данных
    # Для заглушки просто перенаправляем обратно на детальную страницу
    
    # Получаем комментарий из формы
    comment = request.form.get('comment', '')
    
    # Здесь должен быть код для обновления статуса отчета в базе данных
    # Например: report.status = 'approved', report.approval_comment = comment
    
    # После подтверждения перенаправляем на страницу фотоотчета
    return redirect(url_for('admin.photo_report_detail', report_id=report_id))

@bp.route('/photos/<int:report_id>/reject', methods=['POST'])
def reject_photo_report(report_id):
    # В реальном приложении здесь будет обновление статуса в базе данных
    # Для заглушки просто перенаправляем обратно на детальную страницу
    
    # Получаем причину отклонения из формы
    rejection_reason = request.form.get('rejection_reason', '')
    
    # Проверяем, что причина отклонения не пустая
    if not rejection_reason:
        # Если причина не указана, возвращаемся назад с сообщением об ошибке
        # В реальном приложении здесь должна быть обработка ошибки
        return redirect(url_for('admin.photo_report_detail', report_id=report_id))
    
    # Здесь должен быть код для обновления статуса отчета в базе данных
    # Например: report.status = 'rejected', report.rejection_reason = rejection_reason
    
    # После отклонения перенаправляем на страницу фотоотчета
    return redirect(url_for('admin.photo_report_detail', report_id=report_id))

@bp.route('/chat/message/<int:message_id>/block', methods=['POST'])
def block_chat_message(message_id):
    # В реальном приложении здесь будет обновление статуса в базе данных
    
    # Получаем причину блокировки из формы
    block_reason = request.form.get('block_reason', '')
    
    # Проверяем, что причина блокировки не пустая
    if not block_reason:
        # Если причина не указана, возвращаемся назад с сообщением об ошибке
        # В реальном приложении здесь должна быть обработка ошибки
        return redirect(url_for('admin.chat'))
    
    # Здесь должен быть код для обновления статуса сообщения в базе данных
    # Например: message.status = 'blocked', message.block_reason = block_reason
    
    # После блокировки перенаправляем на страницу модерации чата
    return redirect(url_for('admin.chat'))

@bp.route('/chat/message/<int:message_id>/unblock', methods=['POST'])
def unblock_chat_message(message_id):
    # В реальном приложении здесь будет обновление статуса в базе данных
    
    # Здесь должен быть код для обновления статуса сообщения в базе данных
    # Например: message.status = 'active', message.block_reason = None
    
    # После разблокировки перенаправляем на страницу модерации чата
    return redirect(url_for('admin.chat'))

@bp.route('/chat/message/<int:message_id>/flag', methods=['POST'])
def flag_chat_message(message_id):
    # В реальном приложении здесь будет обновление статуса в базе данных
    
    # Получаем причину пометки из формы
    flag_reason = request.form.get('flag_reason', '')
    
    # Здесь должен быть код для обновления статуса сообщения в базе данных
    # Например: message.status = 'flagged', message.flag_reason = flag_reason
    
    # После пометки перенаправляем на страницу модерации чата
    return redirect(url_for('admin.chat'))

@bp.route('/chat/message/<int:message_id>/unflag', methods=['POST'])
def unflag_chat_message(message_id):
    # В реальном приложении здесь будет обновление статуса в базе данных
    
    # Здесь должен быть код для обновления статуса сообщения в базе данных
    # Например: message.status = 'active', message.flag_reason = None
    
    # После снятия пометки перенаправляем на страницу модерации чата
    return redirect(url_for('admin.chat'))

@bp.route('/profile')
def admin_profile():
    # Заглушка для данных профиля администратора
    admin_info = {
        'name': 'Администратор',
        'initials': 'АД',
        'email': 'admin@mastodontco.com',
        'phone': '+7 (900) 111-22-33',
        'role': 'Администратор',
        'registered_at': '01.01.2023',
        'last_login': datetime.now().strftime('%d.%m.%Y %H:%M'),
        'permissions': [
            'Управление пользователями',
            'Управление объектами',
            'Модерация документов',
            'Модерация фотоотчетов',
            'Модерация чата'
        ],
        'activity': [
            {
                'action': 'Создал пользователя',
                'target': 'Иван Петров',
                'date': (datetime.now() - timedelta(days=1)).strftime('%d.%m.%Y %H:%M')
            },
            {
                'action': 'Одобрил фотоотчет',
                'target': 'ЖК "Солнечный"',
                'date': (datetime.now() - timedelta(days=2)).strftime('%d.%m.%Y %H:%M')
            },
            {
                'action': 'Удалил сообщение',
                'target': 'Чат ЖК "Парковый"',
                'date': (datetime.now() - timedelta(days=3)).strftime('%d.%m.%Y %H:%M')
            }
        ]
    }
    
    # Данные для настройки меню
    admin_endpoints = {
        'admin.index': True,
        'admin.users': True,
        'admin.objects': True,
        'admin.docs': True,
        'admin.photos': True,
        'admin.chat': True
    }
    
    return render_template(
        'admin/profile.html',
        admin=admin_info,
        config={'ADMIN_ENDPOINTS': admin_endpoints}
    )

@bp.route('/users/pending')
def pending_users():
    # Получаем всех пользователей со статусом 'pending'
    pending_users = User.query.filter_by(status='pending').all()
    
    return render_template(
        'admin/pending_users.html',
        users=pending_users
    )

@bp.route('/users/<int:user_id>/approve', methods=['POST'])
def approve_user(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'approved'
    db.session.commit()
    
    flash(f'Пользователь {user.username} успешно подтвержден', 'success')
    return redirect(url_for('admin.pending_users'))

@bp.route('/users/<int:user_id>/reject', methods=['POST'])
def reject_user(user_id):
    user = User.query.get_or_404(user_id)
    user.status = 'rejected'
    db.session.commit()
    
    flash(f'Регистрация пользователя {user.username} отклонена', 'success')
    return redirect(url_for('admin.pending_users'))
