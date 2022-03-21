from typing import Dict
from usermodel.models import User
from cart.models import Order, OrderProduct
from product.models import Product
from cart.enums import OrderStatus
import random
import string
import datetime

class OrderService:
    def __init__(self, user: User):
        self.user = user
    
    def create_code(self, length: int = 6):
        current_date = str(datetime.date.today().strftime("%d/%m/%Y")).replace("/", "")
        code = ''.join((random.choice(string.ascii_uppercase) for x in range(length))) + current_date
        check_order = Order.objects.filter(code=code).exists()
        while check_order:
            code, checked = self.create_code()
            if checked:
                check_order = False
        return code, True     
    
    def create_order_if_not_exists(self):
        order, created = Order.objects.get_or_create(user=self.user, status=OrderStatus.IS_SHOPPING, defaults={})
        return order
    
    # transfer products which not bought by user to a new order after User ordered
    def transfer_products_not_buy_to_new_order(self, order: Order, list_products: list[Dict]):
        order_product = OrderProduct.objects.filter(order=order)
        product_ids = [int(product["product_id"]) for product in list_products]
        products = Product.objects.filter(id__in=product_ids)
        
        for product in list_products:
            for op in order_product:
                if op.product_id == product["product_id"]:
                    op.amount = product["amount"]
                    op.total = op.amount * op.price
                    op.is_buying = True
                    break
            for p in products:
                if product["product_id"] == p.id:
                    p.amount= p.amount - product["amount"]
                    break
        OrderProduct.objects.bulk_update(order_product, fields=["is_buying", "amount", "total"])
        Product.objects.bulk_update(products, fields=["amount"])
        
        not_order_product = OrderProduct.objects.filter(order=order, is_buying=False)
        new_order = self.create_order_if_not_exists()
        #transfer products was bought into new order
        not_order_product.update(order=new_order)
        
        return order_product
        
    