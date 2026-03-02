from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, FloatField, TextAreaField, SubmitField, FieldList
from wtforms.validators import DataRequired, Length, Optional
from app.utils.image_processor import get_allowed_extensions


# Obtener extensiones permitidas dinámicamente
ALLOWED_EXTENSIONS = get_allowed_extensions()
EXTENSIONS_STRING = ', '.join(ext.upper() for ext in ALLOWED_EXTENSIONS)


class ProductUploadForm(FlaskForm):
    """Formulario para subir nuevos productos."""
    name = StringField('Nombre del Producto', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(max=100, message='Máximo 100 caracteres')
    ])
    price = FloatField('Precio (€)', validators=[
        DataRequired(message='El precio es requerido'),
    ])
    description = TextAreaField('Descripción', validators=[
        DataRequired(message='La descripción es requerida'),
        Length(max=1000, message='Máximo 1000 caracteres')
    ])
    # Campo principal obligatorio
    image = FileField('Imagen Principal *', validators=[
        FileRequired(message='Debe seleccionar al menos una imagen principal'),
        FileAllowed(ALLOWED_EXTENSIONS, f'Solo: {EXTENSIONS_STRING}')
    ])
    # Campos adicionales opcionales (hasta 4 más)
    image2 = FileField('Imagen 2 (Opcional)', validators=[
        FileAllowed(ALLOWED_EXTENSIONS, f'Solo: {EXTENSIONS_STRING}')
    ])
    image3 = FileField('Imagen 3 (Opcional)', validators=[
        FileAllowed(ALLOWED_EXTENSIONS, f'Solo: {EXTENSIONS_STRING}')
    ])
    image4 = FileField('Imagen 4 (Opcional)', validators=[
        FileAllowed(ALLOWED_EXTENSIONS, f'Solo: {EXTENSIONS_STRING}')
    ])
    image5 = FileField('Imagen 5 (Opcional)', validators=[
        FileAllowed(ALLOWED_EXTENSIONS, f'Solo: {EXTENSIONS_STRING}')
    ])
    submit = SubmitField('Guardar Producto')
