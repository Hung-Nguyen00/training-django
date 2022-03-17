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
    def transfer_products_not_buy_to_new_order(self, order: Order):
        order_product = OrderProduct.objects.filter(order=order)
        ordered_product = order_product.filter(is_buying=True).values("product_id", "amount")
        not_order_product = order_product.filter(is_buying=False)
        product_ids = [details["product_id"] for details in ordered_product]
        products = Product.objects.filter(id__in=product_ids)
        
        new_order = self.create_order_if_not_exists()
        #transfer products was bought into new order
        not_order_product.update(order=new_order)
        
        for details in ordered_product:
            for product in products:
                if details["product_id"] == product.id:
                    product.amount= product.amount - details["amount"]
                    break
                    
        Product.objects.bulk_update(products, fields=["amount"])
        return order_product
        
    