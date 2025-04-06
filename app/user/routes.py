from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from app.user import bp
from datetime import datetime, timedelta
from app.auth.decorators import approval_required

@bp.route('/')
@login_required
@approval_required
def index():
    # Заглушка для данных главной страницы
    user_info = {
        'name': 'Иван Петров',
        'role': 'Менеджер',
        'initials': 'ИП',
        'avatar': None
    }
    
    # Информация о недавних объектах
    recent_objects = [
        {
            'id': 1,
            'name': 'ЖК "Солнечный"',
            'address': 'г. Москва, ул. Солнечная, 12',
            'status': 'active',
            'status_display': 'Активный',
            'progress': 45,
            'image': None
        },
        {
            'id': 2,
            'name': 'ЖК "Морской"',
            'address': 'г. Сочи, ул. Приморская, 24',
            'status': 'construction',
            'status_display': 'Строительство',
            'progress': 70,
            'image': None
        },
        {
            'id': 3,
            'name': 'ЖК "Парковый"',
            'address': 'г. Екатеринбург, пр. Ленина, 56',
            'status': 'planning',
            'status_display': 'Проектирование',
            'progress': 15,
            'image': None
        }
    ]
    
    # Недавние уведомления
    recent_notifications = [
        {
            'id': 1,
            'title': 'Новый документ загружен',
            'description': 'Документ "Разрешение на строительство" добавлен в ЖК "Солнечный"',
            'time': '2 часа назад',
            'is_read': False
        },
        {
            'id': 2,
            'title': 'Фотоотчет утвержден',
            'description': 'Ваш фотоотчет "Заливка фундамента, блок А" был утвержден',
            'time': 'Вчера',
            'is_read': True
        },
        {
            'id': 3,
            'title': 'Новое сообщение',
            'description': 'У вас новое сообщение от Анны Смирновой по объекту ЖК "Морской"',
            'time': '3 дня назад',
            'is_read': True
        }
    ]
    
    # Статистика для пользователя
    stats = {
        'objects_count': 5,
        'documents_count': 27,
        'photos_count': 12,
        'messages_count': 48
    }
    
    # Предстоящие задачи
    upcoming_tasks = [
        {
            'id': 1,
            'title': 'Загрузить фотоотчет',
            'object': 'ЖК "Солнечный"',
            'deadline': 'Сегодня',
            'priority': 'high'
        },
        {
            'id': 2,
            'title': 'Подписать договор с подрядчиком',
            'object': 'ЖК "Парковый"',
            'deadline': 'Завтра',
            'priority': 'medium'
        },
        {
            'id': 3,
            'title': 'Проверить качество отделки',
            'object': 'ЖК "Морской"',
            'deadline': '3 дня',
            'priority': 'low'
        }
    ]
    
    return render_template(
        'user/index.html',
        user=user_info,
        recent_objects=recent_objects,
        recent_notifications=recent_notifications,
        stats=stats,
        upcoming_tasks=upcoming_tasks
    )

@bp.route('/objects')
@login_required
@approval_required
def objects():
    # Заглушка для списка объектов
    objects_list = [
        {
            'id': 1,
            'name': 'ЖК "Солнечный"',
            'address': 'г. Москва, ул. Солнечная, 12',
            'status': 'active',
            'status_display': 'Активный',
            'progress': 45,
            'start_date': '10.01.2023',
            'end_date': '15.12.2023',
            'manager': {
                'name': 'Иван Петров',
                'initials': 'ИП',
                'avatar': None
            },
            'image': None,
            'documents_count': 12,
            'photos_count': 5
        },
        {
            'id': 2,
            'name': 'ЖК "Морской"',
            'address': 'г. Сочи, ул. Приморская, 24',
            'status': 'construction',
            'status_display': 'Строительство',
            'progress': 70,
            'start_date': '05.03.2022',
            'end_date': '30.06.2023',
            'manager': {
                'name': 'Анна Смирнова',
                'initials': 'АС',
                'avatar': None
            },
            'image': None,
            'documents_count': 8,
            'photos_count': 7
        },
        {
            'id': 3,
            'name': 'ЖК "Парковый"',
            'address': 'г. Екатеринбург, пр. Ленина, 56',
            'status': 'planning',
            'status_display': 'Проектирование',
            'progress': 15,
            'start_date': '01.04.2023',
            'end_date': '31.03.2024',
            'manager': {
                'name': 'Сергей Иванов',
                'initials': 'СИ',
                'avatar': None
            },
            'image': None,
            'documents_count': 5,
            'photos_count': 2
        },
        {
            'id': 4,
            'name': 'ЖК "Ясный"',
            'address': 'г. Казань, ул. Ясная, 8',
            'status': 'completed',
            'status_display': 'Завершен',
            'progress': 100,
            'start_date': '15.05.2022',
            'end_date': '10.04.2023',
            'manager': {
                'name': 'Мария Козлова',
                'initials': 'МК',
                'avatar': None
            },
            'image': None,
            'documents_count': 15,
            'photos_count': 10
        },
        {
            'id': 5,
            'name': 'ЖК "Центральный"',
            'address': 'г. Новосибирск, ул. Центральная, 15',
            'status': 'paused',
            'status_display': 'Приостановлен',
            'progress': 60,
            'start_date': '20.02.2022',
            'end_date': '25.12.2023',
            'manager': {
                'name': 'Дмитрий Соколов',
                'initials': 'ДС',
                'avatar': None
            },
            'image': None,
            'documents_count': 7,
            'photos_count': 4
        }
    ]
    
    return render_template(
        'user/objects.html',
        objects=objects_list
    )

@bp.route('/objects/<int:object_id>')
@login_required
@approval_required
def object_detail(object_id):
    # Заглушка для конкретного объекта
    objects_list = [
        {
            'id': 1,
            'name': 'ЖК "Солнечный"',
            'address': 'г. Москва, ул. Солнечная, 12',
            'status': 'active',
            'status_display': 'Активный',
            'progress': 45,
            'start_date': '10.01.2023',
            'end_date': '15.12.2023',
            'description': 'Жилой комплекс "Солнечный" - современный комплекс с развитой инфраструктурой, расположенный в экологически чистом районе города.',
            'manager': {
                'name': 'Иван Петров',
                'initials': 'ИП',
                'avatar': None,
                'phone': '+7 (900) 123-45-67',
                'email': 'i.petrov@example.com'
            },
            'area': '12 500 м²',
            'floors': '24',
            'apartments': '360',
            'parking': '400 мест',
            'image': None,
            'stages': [
                {
                    'name': 'Проектирование',
                    'status': 'completed',
                    'progress': 100
                },
                {
                    'name': 'Фундамент',
                    'status': 'completed',
                    'progress': 100
                },
                {
                    'name': 'Каркас здания',
                    'status': 'in_progress',
                    'progress': 65
                },
                {
                    'name': 'Инженерные системы',
                    'status': 'in_progress',
                    'progress': 30
                },
                {
                    'name': 'Отделка',
                    'status': 'not_started',
                    'progress': 0
                },
                {
                    'name': 'Благоустройство',
                    'status': 'not_started',
                    'progress': 0
                }
            ],
            'recent_activities': [
                {
                    'description': 'Загружен новый документ: "Разрешение на строительство"',
                    'date': '20.04.2023',
                    'user': {
                        'name': 'Иван Петров',
                        'initials': 'ИП'
                    }
                },
                {
                    'description': 'Обновлен статус этапа: "Каркас здания" - 65%',
                    'date': '18.04.2023',
                    'user': {
                        'name': 'Анна Смирнова',
                        'initials': 'АС'
                    }
                },
                {
                    'description': 'Загружен фотоотчет: "Монтаж перекрытий 3-го этажа"',
                    'date': '15.04.2023',
                    'user': {
                        'name': 'Сергей Иванов',
                        'initials': 'СИ'
                    }
                }
            ]
        }
    ]
    
    # Находим объект по ID
    object_info = None
    for obj in objects_list:
        if obj['id'] == object_id:
            object_info = obj
            break
    
    if not object_info:
        # Если объект не найден, перенаправляем на список объектов
        flash('Объект не найден', 'error')
        return redirect(url_for('user.objects'))
    
    return render_template(
        'user/object_detail.html',
        object=object_info
    )

@bp.route('/documents')
@login_required
@approval_required
def documents():
    # Заглушка для списка документов
    documents_list = [
        {
            'id': 1,
            'name': 'Договор подряда',
            'object_id': 1,
            'object_name': 'ЖК "Солнечный"',
            'doc_type': 'contract',
            'doc_type_display': 'Договор',
            'file_extension': 'pdf',
            'type': 'pdf',
            'size': '2.5 МБ',
            'uploaded_at': '15.01.2023',
            'uploaded_by': {
                'name': 'Иван Петров',
                'initials': 'ИП'
            }
        },
        {
            'id': 2,
            'name': 'Разрешение на строительство',
            'object_id': 1,
            'object_name': 'ЖК "Солнечный"',
            'doc_type': 'permit',
            'doc_type_display': 'Разрешение',
            'file_extension': 'pdf',
            'type': 'pdf',
            'size': '1.2 МБ',
            'uploaded_at': '20.01.2023',
            'uploaded_by': {
                'name': 'Иван Петров',
                'initials': 'ИП'
            }
        },
        {
            'id': 3,
            'name': 'План первого этажа',
            'object_id': 1,
            'object_name': 'ЖК "Солнечный"',
            'doc_type': 'plan',
            'doc_type_display': 'План',
            'file_extension': 'dwg',
            'type': 'dwg',
            'size': '5.8 МБ',
            'uploaded_at': '25.01.2023',
            'uploaded_by': {
                'name': 'Сергей Иванов',
                'initials': 'СИ'
            }
        },
        {
            'id': 4,
            'name': 'Ежемесячный отчет Январь 2023',
            'object_id': 2,
            'object_name': 'ЖК "Морской"',
            'doc_type': 'report',
            'doc_type_display': 'Отчет',
            'file_extension': 'docx',
            'type': 'docx',
            'size': '3.7 МБ',
            'uploaded_at': '05.02.2023',
            'uploaded_by': {
                'name': 'Анна Смирнова',
                'initials': 'АС'
            }
        },
        {
            'id': 5,
            'name': 'Спецификация материалов',
            'object_id': 3,
            'object_name': 'ЖК "Парковый"',
            'doc_type': 'other',
            'doc_type_display': 'Прочее',
            'file_extension': 'xlsx',
            'type': 'xlsx',
            'size': '1.9 МБ',
            'uploaded_at': '10.02.2023',
            'uploaded_by': {
                'name': 'Мария Козлова',
                'initials': 'МК'
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
    
    return render_template(
        'user/documents.html',
        documents=documents_list,
        objects=objects
    )

@bp.route('/photos')
@login_required
@approval_required
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
    
    return render_template(
        'user/photos.html',
        photo_reports=photo_reports,
        objects=objects
    )

@bp.route('/photos/<int:report_id>')
@login_required
@approval_required
def photo_report_detail(report_id):
    # Заглушка для детальной информации о фотоотчете
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
        }
    ]
    
    # Находим отчет по ID
    report = None
    for r in all_reports:
        if r['id'] == report_id:
            report = r
            break
    
    if not report:
        # Если отчет не найден, перенаправляем на список отчетов
        flash('Фотоотчет не найден', 'error')
        return redirect(url_for('user.photos'))
    
    return render_template(
        'user/photo_detail.html',
        report=report
    )

@bp.route('/profile')
@login_required
@approval_required
def profile():
    # Заглушка для данных профиля пользователя
    user_info = {
        'name': 'Иван Петров',
        'email': 'i.petrov@example.com',
        'role': 'Менеджер',
        'avatar': None,
        'phone': '+7 (900) 123-45-67',
        'registered': '15.01.2023'
    }
    
    # Настройки пользователя
    user_settings = {
        'email_notifications': True,
        'document_updates': True,
        'photo_reports': True,
        'messages': True,
        'task_reminders': False
    }
    
    # Последние действия пользователя
    activity_log = [
        {
            'action': 'Загрузил документ',
            'target': 'План строительства.pdf',
            'date': '04.04.2023'
        },
        {
            'action': 'Добавил комментарий',
            'target': 'ЖК "Морской"',
            'date': '01.04.2023'
        },
        {
            'action': 'Создал фотоотчет',
            'target': 'Прокладка коммуникаций (ЖК "Солнечный")',
            'date': '25.03.2023'
        }
    ]
    
    return render_template(
        'user/profile.html',
        user=user_info,
        user_settings=user_settings,
        activity_log=activity_log
    )

@bp.route('/settings')
@login_required
@approval_required
def settings():
    # Заглушка для настроек пользователя
    user_info = {
        'name': 'Иван Петров',
        'email': 'i.petrov@example.com',
        'phone': '+7 (900) 123-45-67',
        'avatar': None
    }
    
    # Настройки пользователя
    user_settings = {
        # Общие настройки
        'language': 'ru',
        'timezone': 'Europe/Moscow',
        'date_format': 'DD.MM.YYYY',
        'autosave': True,
        
        # Настройки уведомлений
        'email_notifications': True,
        'push_notifications': True,
        'sms_notifications': False,
        'document_updates': True,
        'photo_reports': True,
        'messages': True,
        'task_reminders': False,
        
        # Подробные настройки уведомлений
        'notifications': {
            'email_new_doc': True,
            'email_new_photo': True,
            'email_comments': False,
            'email_status_changes': True,
            'push_new_doc': True,
            'push_messages': True
        }
    }
    
    # История входов
    login_history = [
        {
            'date': '23.04.2023 14:32',
            'ip': '192.168.1.1',
            'device': 'Chrome на Windows',
            'location': 'Москва, Россия'
        },
        {
            'date': '20.04.2023 09:15',
            'ip': '192.168.1.1',
            'device': 'Safari на iPhone',
            'location': 'Москва, Россия'
        },
        {
            'date': '15.04.2023 18:45',
            'ip': '192.168.1.1',
            'device': 'Firefox на MacOS',
            'location': 'Санкт-Петербург, Россия'
        }
    ]
    
    # Активные сессии
    active_sessions = [
        {
            'device_type': 'desktop',
            'browser': 'Chrome',
            'os': 'Windows',
            'ip': '192.168.1.1',
            'location': 'Москва, Россия',
            'last_active': '23.04.2023 14:32'
        },
        {
            'device_type': 'mobile',
            'browser': 'Safari',
            'os': 'iOS',
            'ip': '192.168.1.1',
            'location': 'Москва, Россия',
            'last_active': '23.04.2023 10:15'
        }
    ]
    
    return render_template(
        'user/settings.html',
        user=user_info,
        user_settings=user_settings,
        notification_settings=user_settings,
        login_history=login_history,
        active_sessions=active_sessions
    )

@bp.route('/privacy-policy')
def privacy_policy():
    return render_template('user/privacy_policy.html')

@bp.route('/terms-of-service')
def terms_of_service():
    return render_template('user/terms_of_service.html') 