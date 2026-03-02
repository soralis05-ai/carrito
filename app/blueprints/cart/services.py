# simple service stub for cart operations

class CartService:
    @staticmethod
    def get_cart_items():
        return []

    @staticmethod
    def calculate_total():
        return 0

    @staticmethod
    def add_item(product_id, quantity=1):
        pass

    @staticmethod
    def remove_item(item_id):
        pass
