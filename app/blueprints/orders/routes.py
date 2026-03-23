from flask import render_template, redirect, url_for, flash, request, session, send_file, current_app
from flask_login import current_user
from . import orders_bp
from app import db
from app.models import Product, Order, OrderItem, CartItem
from datetime import datetime
import uuid
import os
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT


@orders_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Página de checkout para finalizar compra."""
    # Obtener items del carrito
    user_id = current_user.id if current_user.is_authenticated else None
    session_id = session.get('session_id')
    
    if not session_id and not user_id:
        session['session_id'] = str(uuid.uuid4())
        session_id = session['session_id']
    
    cart_items = CartItem.query.filter(
        (CartItem.user_id == user_id) | (CartItem.session_id == session_id)
    ).all()
    
    if not cart_items:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('cart.view_cart'))
    
    # Calcular totales
    subtotal = sum(item.subtotal for item in cart_items)
    shipping_cost = 0  # Envío gratis
    tax = subtotal * 0.21  # 21% IVA
    total = subtotal + shipping_cost + tax
    
    if request.method == 'POST':
        # Obtener datos del formulario
        shipping_data = {
            'name': request.form.get('name', ''),
            'email': request.form.get('email', ''),
            'phone': request.form.get('phone', ''),
            'address': request.form.get('address', ''),
            'city': request.form.get('city', ''),
            'zip': request.form.get('zip', ''),
            'country': request.form.get('country', 'España'),
            'notes': request.form.get('notes', ''),
        }
        
        # Validar datos requeridos
        required_fields = ['name', 'email', 'phone', 'address', 'city', 'zip']
        missing_fields = [f for f in required_fields if not shipping_data.get(f)]
        
        if missing_fields:
            flash(f'Por favor completa los campos requeridos: {", ".join(missing_fields)}', 'danger')
            return render_template('orders/checkout.html', 
                                 cart_items=cart_items,
                                 subtotal=subtotal,
                                 shipping_cost=shipping_cost,
                                 tax=tax,
                                 total=total,
                                 shipping=shipping_data)
        
        # Crear pedido
        order = Order()
        order.order_number = f"PED-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        if user_id:
            order.user_id = user_id
        else:
            order.guest_email = shipping_data['email']
        
        order.status = Order.STATUS_PENDING
        order.shipping_name = shipping_data['name']
        order.shipping_email = shipping_data['email']
        order.shipping_phone = shipping_data['phone']
        order.shipping_address = shipping_data['address']
        order.shipping_city = shipping_data['city']
        order.shipping_zip = shipping_data['zip']
        order.shipping_country = shipping_data['country']
        order.shipping_notes = shipping_data['notes']
        order.subtotal = subtotal
        order.shipping_cost = shipping_cost
        order.tax = tax
        order.total = total
        order.payment_method = 'pending'
        order.payment_status = 'pending'
        
        db.session.add(order)
        db.session.flush()  # Obtener ID
        
        # Crear items del pedido
        for cart_item in cart_items:
            product = cart_item.product
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                product_name=product.name,
                product_sku=product.sku,
                quantity=cart_item.quantity,
                unit_price=product.price,
                total=cart_item.subtotal
            )
            db.session.add(order_item)
        
        # Eliminar items del carrito
        for cart_item in cart_items:
            db.session.delete(cart_item)
        
        db.session.commit()
        
        flash(f'¡Pedido confirmado! Número: {order.order_number}', 'success')
        return redirect(url_for('orders.confirmation', order_id=order.id))
    
    return render_template('orders/checkout.html',
                         cart_items=cart_items,
                         subtotal=subtotal,
                         shipping_cost=shipping_cost,
                         tax=tax,
                         total=total)
    """Generar PDF de oferta del pedido."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=0.5*inch, leftMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("OFERTA COMERCIAL", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Información del pedido
    info_style = ParagraphStyle(
        'OrderInfo',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER
    )
    elements.append(Paragraph(f"<b>Número de Pedido:</b> {order.order_number}", info_style))
    elements.append(Paragraph(f"<b>Fecha:</b> {order.created_at.strftime('%d/%m/%Y %H:%M')}", info_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Datos de envío
    shipping_style = ParagraphStyle(
        'Shipping',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_LEFT
    )
    elements.append(Paragraph("<b>Datos de Envío:</b>", shipping_style))
    elements.append(Paragraph(f"{order.shipping_address}", shipping_style))
    elements.append(Paragraph(f"{order.shipping_zip}, {order.shipping_city}", shipping_style))
    elements.append(Paragraph(f"{order.shipping_country}", shipping_style))
    elements.append(Paragraph(f"Teléfono: {order.shipping_phone}", shipping_style))
    if order.guest_email:
        elements.append(Paragraph(f"Email: {order.guest_email}", shipping_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Tabla de productos
    data = [['Producto', 'Cant.', 'Precio Unit.', 'Total']]
    
    for item in order.items:
        data.append([
            item.product_name,
            str(item.quantity),
            f"€{float(item.unit_price):.2f}",
            f"€{float(item.total):.2f}"
        ])
    
    table = Table(data, colWidths=[3*inch, 0.7*inch, 1*inch, 1*inch])
    table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        # Filas
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Totales
    totals_style = ParagraphStyle(
        'Totals',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_LEFT
    )
    total_bold = ParagraphStyle(
        'TotalBold',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#667eea'),
        alignment=TA_LEFT
    )
    
    elements.append(Paragraph(f"<b>Total Productos:</b> €{float(order.subtotal):.2f}", totals_style))
    if order.shipping_cost > 0:
        elements.append(Paragraph(f"<b>Envío:</b> €{float(order.shipping_cost):.2f}", totals_style))
    else:
        elements.append(Paragraph(f"<b>Envío:</b> GRATIS", totals_style))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(f"<b>TOTAL:</b> €{float(order.total):.2f}", total_bold))
    elements.append(Spacer(1, 0.5*inch))

    # Nota al pie
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("<i>* Precios con IVA incluido</i>", footer_style))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("Esta oferta es válida por 7 días desde la fecha de emisión.", footer_style))
    elements.append(Paragraph("Gracias por su compra - Almapunt", footer_style))
    
    # Construir PDF
    doc.build(elements)
    buffer.seek(0)

    return buffer


@orders_bp.route('/confirmation/<int:order_id>')
def confirmation(order_id):
    """Página de confirmación de pedido."""
    order = Order.query.get_or_404(order_id)
    return render_template('orders/confirmation.html', order=order)


@orders_bp.route('/download-offer/<int:order_id>')
def download_offer(order_id):
    """Descargar oferta en PDF."""
    order = Order.query.get_or_404(order_id)
    
    # Verificar que el usuario puede acceder al pedido
    if current_user.is_authenticated:
        if order.user_id != current_user.id:
            flash('No tienes permiso para acceder a este pedido', 'danger')
            return redirect(url_for('products.list'))
    
    # Generar PDF
    pdf_buffer = generate_order_pdf(order)
    
    filename = f"oferta-{order.order_number}.pdf"
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )
