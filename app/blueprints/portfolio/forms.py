from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Optional
from app.utils.image_processor import get_allowed_extensions


ALLOWED_EXTENSIONS = get_allowed_extensions()
EXTENSIONS_STRING = ', '.join(ext.upper() for ext in ALLOWED_EXTENSIONS)


class PortfolioItemForm(FlaskForm):
    """Formulario para subir items al portfolio."""
    title = StringField('Título', validators=[
        DataRequired(message='El título es requerido'),
        Length(max=100, message='Máximo 100 caracteres')
    ])
    description = TextAreaField('Descripción', validators=[
        Optional(),
        Length(max=500, message='Máximo 500 caracteres')
    ])
    image = FileField('Imagen *', validators=[
        FileRequired(message='Debe seleccionar una imagen'),
        FileAllowed(ALLOWED_EXTENSIONS, f'Solo: {EXTENSIONS_STRING}')
    ])
    order = StringField('Orden de visualización', validators=[
        Optional(),
        Length(max=3, message='Máximo 3 dígitos')
    ])
    submit = SubmitField('Guardar Item')


class PortfolioInfoForm(FlaskForm):
    """Formulario para información personal del portfolio."""
    name = StringField('Nombre', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(max=100)
    ])
    title = StringField('Título Profesional', validators=[
        Optional(),
        Length(max=100)
    ])
    bio = TextAreaField('Biografía', validators=[
        Optional(),
        Length(max=1000, message='Máximo 1000 caracteres')
    ])
    email = StringField('Email de Contacto', validators=[
        Optional(),
        Length(max=100)
    ])
    phone = StringField('Teléfono', validators=[
        Optional(),
        Length(max=20)
    ])
    submit = SubmitField('Guardar Información')
