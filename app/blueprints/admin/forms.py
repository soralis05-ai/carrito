from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, FloatField, TextAreaField, SubmitField, FieldList, BooleanField, FormField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from app.utils.image_processor import get_allowed_extensions


# Obtener extensiones permitidas dinámicamente
ALLOWED_EXTENSIONS = get_allowed_extensions()
EXTENSIONS_STRING = ', '.join(ext.upper() for ext in ALLOWED_EXTENSIONS)


class CostosAmigurumiForm(FlaskForm):
    """Formulario para calcular costos de amigurumis."""
    
    # Lana
    lana_costo_rollo = FloatField('Costo del Rollo de Lana (€)', validators=[
        Optional(),
        NumberRange(min=0, message='Debe ser mayor o igual a 0')
    ])
    lana_peso_rollo = FloatField('Peso del Rollo (gramos)', validators=[
        Optional(),
        NumberRange(min=0, message='Debe ser mayor o igual a 0')
    ])
    lana_peso_usado = FloatField('Peso Usado en este producto (gramos)', validators=[
        Optional(),
        NumberRange(min=0, message='Debe ser mayor o igual a 0')
    ])
    
    # Relleno
    relleno_costo_bolsa = FloatField('Costo de la Bolsa de Relleno (€)', validators=[
        Optional(),
        NumberRange(min=0, message='Debe ser mayor o igual a 0')
    ])
    relleno_peso_bolsa = FloatField('Peso de la Bolsa (gramos)', validators=[
        Optional(),
        NumberRange(min=0, message='Debe ser mayor o igual a 0')
    ])
    relleno_peso_usado = FloatField('Peso Usado en este producto (gramos)', validators=[
        Optional(),
        NumberRange(min=0, message='Debe ser mayor o igual a 0')
    ])
    
    # Ojos
    ojos_usar = BooleanField('¿Lleva ojos de seguridad?')
    ojos_costo_unitario = FloatField('Costo por par de ojos (€)', validators=[
        Optional(),
        NumberRange(min=0, message='Debe ser mayor o igual a 0')
    ])
    ojos_cantidad = FloatField('Cantidad de pares de ojos', validators=[
        Optional(),
        NumberRange(min=0, message='Debe ser mayor o igual a 0')
    ])
    
    # Margen de ganancia (porcentaje)
    margen_ganancia = FloatField('Margen de Ganancia (%)', validators=[
        Optional(),
        NumberRange(min=0, max=500, message='Entre 0 y 500%')
    ], default=100)


class ProductUploadForm(FlaskForm):
    """Formulario para subir nuevos productos."""
    name = StringField('Nombre del Producto', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(max=100, message='Máximo 100 caracteres')
    ])
    price = FloatField('Precio de Venta (€)', validators=[
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
    
    # Costos de producción (amigurumis)
    costos = FieldList(FormField(CostosAmigurumiForm), min_entries=1)
    
    submit = SubmitField('Guardar Producto')
