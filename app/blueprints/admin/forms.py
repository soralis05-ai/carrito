from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired, FileStorage
from wtforms import StringField, FloatField, TextAreaField, SubmitField, FieldList, BooleanField, FormField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from app.utils.image_processor import ALLOWED_EXTENSIONS, EXTENSIONS_STRING


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

    # Mano de Obra
    mano_obra_usar = BooleanField('¿Considerar mano de obra?')
    mano_obra_costo_hora = FloatField('Costo por Hora de Trabajo (€)', validators=[
        Optional(),
        NumberRange(min=0, message='Debe ser mayor o igual a 0')
    ])
    mano_obra_horas = FloatField('Horas Dedicadas', validators=[
        Optional(),
        NumberRange(min=0, message='Debe ser mayor o igual a 0')
    ])

    # Utilidad (Opcional)
    utilidad_usar = BooleanField('¿Agregar utilidad adicional?')
    utilidad_porcentaje = FloatField('Porcentaje de Utilidad (%)', validators=[
        Optional(),
        NumberRange(min=0, max=500, message='Entre 0 y 500%')
    ])


class ProductUploadForm(FlaskForm):
    """Formulario para subir nuevos productos."""
    # Información básica
    name = StringField('Nombre del Producto', validators=[
        DataRequired(message='El nombre es requerido'),
        Length(max=200, message='Máximo 200 caracteres')
    ])
    description = TextAreaField('Descripción', validators=[
        Optional(),  # Opcional para creación rápida
        Length(max=1000, message='Máximo 1000 caracteres')
    ])

    # Precio y stock (opcionales para creación rápida)
    price = FloatField('Precio de Venta (€)', validators=[
        Optional(),  # Opcional para creación rápida
        NumberRange(min=0, message='El precio debe ser mayor o igual a 0')
    ])
    stock = IntegerField('Stock Disponible', validators=[
        Optional(),  # Opcional para creación rápida
        NumberRange(min=0, message='El stock no puede ser negativo')
    ])
    sku = StringField('SKU (Referencia)', validators=[
        Optional(),
        Length(max=50, message='Máximo 50 caracteres')
    ])

    # Categoría
    category_id = SelectField('Categoría', coerce=int, validators=[
        Optional()
    ])

    # Estado
    is_featured = BooleanField('Producto destacado')
    is_active = BooleanField('Producto activo', default=False)  # Desmarcado por defecto

    # Imágenes
    image = FileField('Imagen Principal *', validators=[
        FileRequired(message='Debe seleccionar al menos una imagen principal'),
        FileAllowed(ALLOWED_EXTENSIONS, f'Solo: {EXTENSIONS_STRING}')
    ])
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

    # Costos de amigurumis (embebido)
    lana_costo_rollo = FloatField('Costo del Rollo de Lana (€)', validators=[Optional()])
    lana_peso_rollo = FloatField('Peso del Rollo (gramos)', validators=[Optional()])
    lana_peso_usado = FloatField('Peso Usado (gramos)', validators=[Optional()])

    relleno_costo_bolsa = FloatField('Costo de la Bolsa de Relleno (€)', validators=[Optional()])
    relleno_peso_bolsa = FloatField('Peso de la Bolsa (gramos)', validators=[Optional()])
    relleno_peso_usado = FloatField('Peso Usado (gramos)', validators=[Optional()])

    ojos_usar = BooleanField('¿Lleva ojos de seguridad?')
    ojos_costo_unitario = FloatField('Costo por par de ojos (€)', validators=[Optional()])
    ojos_cantidad = FloatField('Cantidad de pares', validators=[Optional()])

    mano_obra_usar = BooleanField('¿Considerar mano de obra?')
    mano_obra_costo_hora = FloatField('Costo por Hora (€)', validators=[Optional()])
    mano_obra_horas = FloatField('Horas Dedicadas', validators=[Optional()])

    utilidad_usar = BooleanField('¿Agregar utilidad adicional?')
    utilidad_porcentaje = FloatField('Porcentaje de Utilidad (%)', validators=[Optional(), NumberRange(min=0, max=500)])

    submit = SubmitField('Guardar Producto')


class ProductEditForm(ProductUploadForm):
    """Formulario para editar productos (imagen principal opcional)."""
    # Sobrescribir para hacer la imagen principal opcional en edición
    image = FileField('Imagen Principal', validators=[
        FileAllowed(ALLOWED_EXTENSIONS, f'Solo: {EXTENSIONS_STRING}')
    ])
    # El precio puede ser 0 inicialmente porque se calcula automáticamente
    price = FloatField('Precio de Venta (€)', validators=[
        Optional(),
        NumberRange(min=0, message='El precio debe ser mayor o igual a 0')
    ])
