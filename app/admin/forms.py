from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from app.models import User

class ConstructionObjectForm(FlaskForm):
    name = StringField('Название объекта', validators=[DataRequired(), Length(min=3, max=128)])
    address = StringField('Адрес', validators=[DataRequired(), Length(min=3, max=256)])
    description = TextAreaField('Описание', validators=[Optional()])
    status = SelectField('Статус', choices=[
        ('planning', 'Подготовка'),
        ('active', 'Активный'),
        ('construction', 'Строительство'),
        ('paused', 'Приостановлен'),
        ('completed', 'Завершен')
    ], validators=[DataRequired()])
    progress = IntegerField('Прогресс (%)', validators=[NumberRange(min=0, max=100), Optional()], default=0)
    start_date = DateField('Дата начала', validators=[Optional()], format='%Y-%m-%d')
    end_date = DateField('Дата завершения', validators=[Optional()], format='%Y-%m-%d')
    manager_id = SelectField('Менеджер проекта', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Сохранить')
    
    def __init__(self, *args, **kwargs):
        super(ConstructionObjectForm, self).__init__(*args, **kwargs)
        # Динамически добавляем пользователей из базы данных
        self.manager_id.choices = [(u.id, u.username) for u in User.query.filter(User.is_admin == True).all()]

class DocumentForm(FlaskForm):
    name = StringField('Название документа', validators=[DataRequired(), Length(min=3, max=256)])
    object_id = SelectField('Объект', choices=[], coerce=int, validators=[DataRequired()])
    doc_type = SelectField('Тип документа', choices=[
        ('contract', 'Договор'),
        ('permit', 'Разрешение'),
        ('plan', 'План'),
        ('report', 'Отчет'),
        ('other', 'Прочее')
    ], validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[Optional()])
    file = FileField('Файл', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png'], 
                   'Разрешены только файлы PDF, DOC, XLS и изображения!')
    ])
    submit = SubmitField('Загрузить документ') 