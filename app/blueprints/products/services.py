# simple product service stub

class ProductsService:
    @staticmethod
    def get_all():
        # in a production app this would fetch from database
        return [
            {'id': 1, 'name': 'Conejito 1', 'price': '19.99€', 'image': 'conejito1.jpg', 'images': ['conejito1.jpg'], 'description': 'Adorable conejito de peluche suave y acogedor. Perfecto para regalar o decorar tu habitación.'},
            {'id': 2, 'name': 'Conejito 2', 'price': '19.99€', 'image': 'conejito2.jpg', 'images': ['conejito2.jpg'], 'description': 'Conejito esponjoso con detalles únicos. Ideal para niños y amantes de los animales.'},
            {'id': 3, 'name': 'Conejito 3', 'price': '19.99€', 'image': 'conejito3.jpg', 'images': ['conejito3.jpg'], 'description': 'Conejito de peluche de alta calidad, suave al tacto y muy resistente.'},
            {'id': 4, 'name': 'Conejito 4', 'price': '19.99€', 'image': 'conejito4.jpg', 'images': ['conejito4.jpg'], 'description': 'Hermoso conejito con diseño exclusivo. Un regalo perfecto para cualquier ocasión.'},
            {'id': 5, 'name': 'Conejito 5', 'price': '19.99€', 'image': 'conejito5.jpg', 'images': ['conejito5.jpg'], 'description': 'Conejito tierno y delicado, fabricado con materiales seguros y duraderos.'},
            {'id': 6, 'name': 'Dientes de Sable', 'price': '24.99€', 'image': 'dientesdesable.jpg', 'images': ['dientesdesable.jpg'], 'description': 'Impresionante figura de dientes de sable. Perfecto para coleccionistas y amantes de la prehistoria.'},
            {'id': 7, 'name': 'Dino 1', 'price': '22.99€', 'image': 'dino1.jpg', 'images': ['dino1.jpg'], 'description': 'Divertido dinosaurio de peluche. Ideal para niños curiosos y fans de los dinosaurios.'},
            {'id': 8, 'name': 'Dino 2', 'price': '22.99€', 'image': 'dino2.jpg', 'images': ['dino2.jpg'], 'description': 'Dinosaurio de diseño único con colores vibrantes y textura suave.'},
            {'id': 9, 'name': 'Dino 3', 'price': '22.99€', 'image': 'dino3.jpg', 'images': ['dino3.jpg'], 'description': 'Dinosaurio de peluche de gran calidad. Un compañero perfecto para aventuras.'},
            {'id': 10, 'name': 'Forro Cuaderno 1', 'price': '9.99€', 'image': 'forrocuaderno1.jpg', 'images': ['forrocuaderno1.jpg'], 'description': 'Forro protector para cuadernos con diseño atractivo. Mantiene tus apuntes seguros y con estilo.'},
            {'id': 11, 'name': 'Forro Cuaderno 2', 'price': '9.99€', 'image': 'forrocuaderno2.jpg', 'images': ['forrocuaderno2.jpg'], 'description': 'Forro resistente y decorativo para tus cuadernos favoritos.'},
            {'id': 12, 'name': 'Forro Cuaderno 3', 'price': '9.99€', 'image': 'forrocuaderno3.jpg', 'images': ['forrocuaderno3.jpg'], 'description': 'Protege tus cuadernos con este forro de diseño único y material duradero.'},
            {'id': 13, 'name': 'Manilla', 'price': '14.99€', 'image': 'manilla1.jpg', 'images': ['manilla1.jpg'], 'description': 'Manilla decorativa de alta calidad. Perfecta para complementar tu estilo personal.'},
            {'id': 14, 'name': 'Monedero 1', 'price': '12.99€', 'image': 'monedero1.jpg', 'images': ['monedero1.jpg'], 'description': 'Monedero compacto y elegante. Ideal para llevar tus monedas y pequeñas pertenencias.'},
            {'id': 15, 'name': 'Monedero 2', 'price': '12.99€', 'image': 'monedero2.jpg', 'images': ['monedero2.jpg'], 'description': 'Monedero práctico con diseño moderno. Espacioso y fácil de transportar.'},
            {'id': 16, 'name': 'Monedero 3', 'price': '12.99€', 'image': 'monedero3.jpg', 'images': ['monedero3.jpg'], 'description': 'Monedero resistente con cierre seguro. Perfecto para el uso diario.'},
            {'id': 17, 'name': 'Muñeca', 'price': '29.99€', 'image': 'muñeca1.jpg', 'images': ['muñeca1.jpg'], 'description': 'Hermosa muñeca artesanal con detalles cuidados. Un regalo especial para niñas y coleccionistas.'},
            {'id': 18, 'name': 'Peaches 1', 'price': '24.99€', 'image': 'peaches1.jpg', 'images': ['peaches1.jpg'], 'description': 'Personaje Peaches de diseño exclusivo. Suave y adorable para todas las edades.'},
            {'id': 19, 'name': 'Peaches 2', 'price': '24.99€', 'image': 'peaches2.jpg', 'images': ['peaches2.jpg'], 'description': 'Peaches de peluche con acabados de calidad. Perfecto para fans de la serie.'},
            {'id': 20, 'name': 'Peaches 3', 'price': '24.99€', 'image': 'peaches3.jpg', 'images': ['peaches3.jpg'], 'description': 'Adorable Peaches con expresión única. Un compañero ideal para jugar o decorar.'},
            {'id': 21, 'name': 'Pollito', 'price': '19.99€', 'image': 'pollito.jpg', 'images': ['pollito.jpg'], 'description': 'Tierno pollito de peluche amarillo. Suave, pequeño y perfecto para regalar.'},
            {'id': 22, 'name': 'Posavasos 1', 'price': '8.99€', 'image': 'posavasos1.jpg', 'images': ['posavasos1.jpg'], 'description': 'Posavasos decorativo que protege tus muebles. Diseño elegante y fácil de limpiar.'},
            {'id': 23, 'name': 'Posavasos 2', 'price': '8.99€', 'image': 'posavasos2.jpg', 'images': ['posavasos2.jpg'], 'description': 'Set de posavasos con estilo único. Ideales para complementar tu decoración.'},
            {'id': 24, 'name': 'Ratón Pérez', 'price': '19.99€', 'image': 'ratonperez.jpg', 'images': ['ratonperez.jpg'], 'description': 'El famoso Ratón Pérez en versión peluche. Perfecto para la tradición de los dientes.'},
            {'id': 25, 'name': 'Tula 1', 'price': '34.99€', 'image': 'tula1.jpg', 'images': ['tula1.jpg'], 'description': 'Muñeca Tula de diseño artesanal. Hecha con materiales de primera calidad.'},
            {'id': 26, 'name': 'Tula 2', 'price': '34.99€', 'image': 'tula2.jpg', 'images': ['tula2.jpg'], 'description': 'Tula con vestido exclusivo. Un regalo inolvidable para ocasiones especiales.'},
            {'id': 27, 'name': 'Varios', 'price': '15.99€', 'image': 'varios.jpg', 'images': ['varios.jpg'], 'description': 'Artículo variado con diseño sorpresa. Calidad garantizada Almapunt.'},
        ]
    
    @staticmethod
    def get_by_id(product_id):
        """Obtener producto por ID."""
        all_products = ProductsService.get_all()
        return next((p for p in all_products if p['id'] == product_id), None)
